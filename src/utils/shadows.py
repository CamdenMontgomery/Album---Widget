from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

# Define a constant for the shade intensity (can be used for other shadows too)
SHADE_INTENSITY = 0
BLUR_RADIUS = 25
X_OFFSET = 0
Y_OFFSET = 0
ALPHA = 50  # Transparency level for the shadow color (0-255)

class MidshadeShadow(QGraphicsDropShadowEffect):
    """
    A custom shadow effect with mid-level shading, designed for UI elements.

    Inherits from QGraphicsDropShadowEffect to provide a soft, diffused shadow
    around a widget. The shadow can be customized by adjusting the parameters.
    """

    def __init__(self):
        super().__init__()

        # Set the shadow properties
        self.setBlurRadius(BLUR_RADIUS)  # Set the blur radius for the shadow
        self.setXOffset(X_OFFSET)        # Set the horizontal offset (X direction)
        self.setYOffset(Y_OFFSET)        # Set the vertical offset (Y direction)
        
        # Set the shadow color with customizable transparency
        self.setColor(QColor(SHADE_INTENSITY, SHADE_INTENSITY, SHADE_INTENSITY, ALPHA))
