"""
Utility for processing and optimizing application icons.
"""
import os
from pathlib import Path
from PyQt5.QtGui import QPixmap, QImage, QBitmap, QRegion, QIcon
from PyQt5.QtCore import Qt

def get_cropped_icon(icon_path: Path) -> QIcon:
    """
    Loads an image, crops internal whitespace, and returns a QIcon.
    Useful for ensuring icons fill the title bar area correctly.
    """
    if not icon_path.exists():
        return QIcon()
        
    pixmap = QPixmap(str(icon_path))
    image = pixmap.toImage()
    
    # --- Smart Crop: Remove internal whitespace ---
    # Try transparency mask first
    mask_img = image.createAlphaMask()
    mask = QBitmap.fromImage(mask_img)
    rect = QRegion(mask).boundingRect()
    
    # If opaque or crop failed, try removing pure white
    if rect.isNull() or (rect.width() >= image.width() - 2 and rect.height() >= image.height() - 2):
        white_mask_img = image.createMaskFromColor(0xFFFFFFFF, Qt.MaskOutColor)
        mask = QBitmap.fromImage(white_mask_img)
        rect = QRegion(mask).boundingRect()
    
    if not rect.isNull() and rect.isValid():
        # Crop the image to the identified logo content
        # Use minimal padding for title bar icons to maximize size
        cropped_image = image.copy(rect)
        pixmap = QPixmap.fromImage(cropped_image)
        
    return QIcon(pixmap)
