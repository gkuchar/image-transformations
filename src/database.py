import sqlite3
import numpy as np
from io import BytesIO
from PIL import Image

class ImageDatabase:
    def __init__(self, db_path="image_collection.db"):
        self.db_path = db_path
        self.create_table()
    
    def create_table(self):
        """Create the images table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caption TEXT NOT NULL,
                image_data BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_image(self, image_array, caption):
        """Save a numpy array image to the database"""
        # Convert numpy array to bytes
        img = Image.fromarray(image_array.astype('uint8'))
        buf = BytesIO()
        img.save(buf, format='PNG')
        image_bytes = buf.getvalue()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO images (caption, image_data) VALUES (?, ?)',
            (caption, image_bytes)
        )
        conn.commit()
        image_id = cursor.lastrowid
        conn.close()
        return image_id
    
    def load_all_images(self):
        """Load all images from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, caption, image_data FROM images ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        images = []
        for row in rows:
            image_id, caption, image_bytes = row
            # Convert bytes back to numpy array
            img = Image.open(BytesIO(image_bytes))
            image_array = np.array(img)
            images.append({
                'id': image_id,
                'caption': caption,
                'image': image_array
            })
        return images
    
    def delete_image(self, image_id):
        """Delete an image from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM images WHERE id = ?', (image_id,))
        conn.commit()
        conn.close()
    
    def get_image_count(self):
        """Get the total number of images in the collection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM images')
        count = cursor.fetchone()[0]
        conn.close()
        return count