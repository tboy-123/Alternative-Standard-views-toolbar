# SPDX-License-Identifier: GPL-3.0-or-later
# Made by Gemini AI Assistant for the IngeTrazo Community..

"""
Alternative Standard Views Toolbar v1.0.0

This extension enhances the IngeTrazo CAD interface by adding:
1. Alternative High-DPI Views Icons: Clean 48px vector matrix mapping with a precise 2px padding for clear visibility on large displays.
2. Unified Projection Cycle Button: Single-click cyclic switching through all 3 camera projection modes (Parallel -> Perspective -> 2-Point Perspective).
3. Smart Zoom Action Button: Intelligent one-click camera framing that prioritizes framing your selected elements, falling back to full model extents if nothing is selected.
4. Independent Theme Toggler Toolbar: Standalone container tool providing instant native Light and Dark theme palette synchronization.
"""

from __future__ import annotations
import math
from pathlib import Path
from PySide6.QtCore import QSize, Qt, QPointF, QRectF
from PySide6.QtGui import QIcon, QAction, QColor, QPixmap, QPainter, QPen, QPolygonF, QBrush, QPainterPath
from PySide6.QtWidgets import QToolBar, QApplication

# Native IngeTrazo core module imports
from views import theme
from core.i18n import tr

PLUGIN_DIR = Path(__file__).parent

def _get_theme_ink() -> QColor:
    """Returns dynamic ink color tracking the active application palette context."""
    return QColor("#E0E0E0") if theme.saved_theme() == theme.DARK else QColor("#231F20")

def _draw_theme_squares_icon() -> QIcon:
    """Draws enlarged overlapping squares with a clean 2px margin on a 48x48 canvas."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    
    painter.setBrush(QColor("#FFFFFF"))
    painter.setPen(QPen(QColor("#252525"), 2.0, Qt.PenStyle.SolidLine))
    painter.drawRect(QRectF(4.0, 4.0, 28.0, 28.0))
    
    painter.setBrush(QColor("#1E1E1E"))
    painter.setPen(QPen(QColor("#FFFFFF"), 2.0, Qt.PenStyle.SolidLine))
    painter.drawRect(QRectF(16.0, 16.0, 28.0, 28.0))
    
    painter.end()
    return QIcon(pm)

def _draw_iso_icon() -> QIcon:
    """Vector canvas for 3D Isometric View icon with shaded components."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setPen(Qt.PenStyle.NoPen)
    
    painter.setBrush(QColor("#0000FF"))
    painter.drawPolygon(QPolygonF([QPointF(24.0, 25.7), QPointF(4.8, 15.1), QPointF(24.0, 4.5), QPointF(43.2, 15.1)]))
    painter.setBrush(QColor("#00FF00"))
    painter.drawPolygon(QPolygonF([QPointF(24.0, 25.7), QPointF(4.8, 15.1), QPointF(4.8, 36.3), QPointF(24.0, 46.9)]))
    painter.setBrush(QColor("#FF0000"))
    painter.drawPolygon(QPolygonF([QPointF(24.0, 25.7), QPointF(24.0, 46.9), QPointF(43.2, 36.3), QPointF(43.2, 15.1)]))
    
    ink = _get_theme_ink()
    painter.setPen(QPen(ink, 1.7, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPolygon(QPolygonF([QPointF(24.0, 4.5), QPointF(4.8, 15.1), QPointF(4.8, 36.3), QPointF(24.0, 46.9), QPointF(43.2, 36.3), QPointF(43.2, 15.1)]))
    
    painter.setPen(QPen(QColor("#1D2733"), 0.8))
    painter.setBrush(QColor("#FFC27D"))
    for pt in [QPointF(24.0, 4.5), QPointF(4.8, 36.3), QPointF(43.2, 36.3)]:
        painter.drawEllipse(pt, 3.5, 3.4)
    painter.end()
    return QIcon(pm)

def _draw_top_icon() -> QIcon:
    """Vector canvas for Top View icon (Perfect 48x48 mapping with 2px padding)."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    ink = _get_theme_ink()
    
    painter.setPen(QPen(ink, 2.1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPolygon(QPolygonF([QPointF(3.9, 15.9), QPointF(16.2, 3.2), QPointF(16.2, 32.4), QPointF(3.9, 45.1)]))
    painter.drawRect(QRectF(16.2, 3.2, 28.5, 29.1))
    painter.drawPolygon(QPolygonF([QPointF(32.4, 15.9), QPointF(44.8, 3.2), QPointF(44.8, 32.4), QPointF(32.4, 45.1)]))
    painter.drawRect(QRectF(3.9, 15.9, 28.5, 29.1))
    
    painter.setBrush(QColor("#1B75BB"))
    painter.drawPolygon(QPolygonF([QPointF(44.8, 3.2), QPointF(16.2, 3.2), QPointF(3.9, 15.9), QPointF(32.4, 15.9)]))
    painter.end()
    return QIcon(pm)

def _draw_bottom_icon() -> QIcon:
    """Vector canvas for Bottom View icon (Perfect 48x48 mapping with 2px padding)."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    ink = _get_theme_ink()
    
    painter.setPen(QPen(ink, 2.1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(QColor("#1B75BB"))
    painter.drawPolygon(QPolygonF([QPointF(44.7, 32.2), QPointF(15.8, 32.2), QPointF(3.3, 44.8), QPointF(32.2, 44.8)]))
    
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPolygon(QPolygonF([QPointF(3.3, 15.8), QPointF(15.8, 3.2), QPointF(15.8, 32.1), QPointF(3.3, 44.7)]))
    painter.drawRect(QRectF(15.8, 3.2, 28.9, 28.9))
    painter.drawPolygon(QPolygonF([QPointF(32.2, 15.8), QPointF(44.7, 3.2), QPointF(44.7, 32.1), QPointF(32.2, 44.7)]))
    painter.drawRect(QRectF(3.3, 15.8, 28.9, 28.9))
    painter.end()
    return QIcon(pm)

def _draw_front_icon() -> QIcon:
    """Vector canvas for Front View icon (Perfect 48x48 mapping with 2px padding)."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    ink = _get_theme_ink()
    
    painter.setPen(QPen(ink, 2.1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPolygon(QPolygonF([QPointF(2.9, 15.9), QPointF(15.7, 3.0), QPointF(15.7, 32.5), QPointF(2.9, 45.4)]))
    painter.drawRect(QRectF(15.7, 3.0, 29.5, 29.5))
    painter.drawPolygon(QPolygonF([QPointF(32.4, 15.9), QPointF(45.2, 3.0), QPointF(45.2, 32.5), QPointF(32.4, 45.4)]))
    
    painter.setBrush(QColor("#37B34A"))
    painter.drawRect(QRectF(2.9, 15.9, 29.5, 29.5))
    painter.end()
    return QIcon(pm)
    
def _draw_back_icon() -> QIcon:
    """Vector canvas for Back View icon (Perfect 48x48 mapping with 2px padding).
    FIXED: Fills the green background first, so wireframe edges correctly render on top.
    """
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    
    # 1. FIRST: Fill the green solid background face at the back layer
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#37B34A"))
    painter.drawRect(QRectF(15.8, 3.5, 28.9, 28.9))
    
    # 2. SECOND: Draw the theme-colored wireframe grid ON TOP of the green face
    ink = _get_theme_ink()
    painter.setPen(QPen(ink, 2.1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    
    painter.drawPolygon(QPolygonF([QPointF(3.3, 16.1), QPointF(15.8, 3.5), QPointF(15.8, 32.5), QPointF(3.3, 45.0)]))
    painter.drawPolygon(QPolygonF([QPointF(32.2, 16.1), QPointF(44.7, 3.5), QPointF(44.7, 32.5), QPointF(32.2, 45.0)]))
    painter.drawRect(QRectF(3.3, 16.1, 28.9, 28.9))
    painter.drawRect(QRectF(15.8, 3.5, 28.9, 28.9)) # Restored frame border definition over fill
    
    painter.end()
    return QIcon(pm)


def _draw_left_icon() -> QIcon:
    """Vector canvas for Left View icon (Perfect 48x48 mapping with 2px padding)."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    ink = _get_theme_ink()
    
    painter.setPen(QPen(ink, 2.1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(QColor("#BE1E2D"))
    painter.drawPolygon(QPolygonF([QPointF(2.9, 15.7), QPointF(15.7, 2.9), QPointF(15.7, 32.3), QPointF(2.9, 45.1)]))
    
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawRect(QRectF(2.9, 15.7, 29.4, 29.4))
    painter.drawRect(QRectF(15.7, 2.9, 29.4, 29.4))
    painter.drawPolygon(QPolygonF([QPointF(32.3, 15.7), QPointF(45.1, 2.9), QPointF(45.1, 32.3), QPointF(32.3, 45.1)]))
    painter.end()
    return QIcon(pm)

def _draw_right_icon() -> QIcon:
    """Vector canvas for Right View icon (Perfect 48x48 mapping with 2px padding)."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    ink = _get_theme_ink()
    
    painter.setPen(QPen(ink, 2.1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPolygon(QPolygonF([QPointF(3.4, 15.9), QPointF(15.8, 3.4), QPointF(15.8, 32.1), QPointF(3.4, 44.6)]))
    painter.drawRect(QRectF(3.4, 15.9, 28.7, 28.7))
    painter.drawRect(QRectF(15.8, 3.4, 28.7, 28.7))
    
    painter.setBrush(QColor("#BE1E2D"))
    painter.drawPolygon(QPolygonF([QPointF(32.2, 15.9), QPointF(44.6, 3.4), QPointF(44.6, 32.1), QPointF(32.2, 44.6)]))
    painter.end()
    return QIcon(pm)

def _draw_proj_parallel_icon() -> QIcon:
    """Vector canvas for Parallel Projection icon (Orthogonal wireframe cube)."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    ink = _get_theme_ink()
    
    painter.setPen(QPen(ink, 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPolyline(QPolygonF([QPointF(12.0, 8.0), QPointF(40.0, 8.0), QPointF(40.0, 34.0)]))
    painter.drawLine(QPointF(12.0, 8.0), QPointF(6.0, 14.0))
    painter.drawLine(QPointF(40.0, 8.0), QPointF(34.0, 14.0))
    painter.drawLine(QPointF(40.0, 34.0), QPointF(34.0, 40.0))
    painter.drawRect(QRectF(6.0, 14.0, 28.0, 26.0))
    painter.end()
    return QIcon(pm)

def _draw_proj_perspective_icon() -> QIcon:
    """Vector canvas for Perspective Projection icon (Vanishing horizon lines)."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    ink = _get_theme_ink()
    
    painter.setPen(QPen(ink, 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPolyline(QPolygonF([QPointF(6.0, 40.0), QPointF(6.0, 16.0), QPointF(28.0, 6.0)]))
    painter.drawPolyline(QPolygonF([QPointF(28.0, 6.0), QPointF(42.0, 6.0), QPointF(42.0, 20.0)]))
    painter.drawPolygon(QPolygonF([QPointF(30.0, 16.0), QPointF(42.0, 6.0), QPointF(42.0, 20.0), QPointF(30.0, 40.0)]))
    painter.drawRect(QRectF(6.0, 16.0, 24.0, 24.0))
    painter.end()
    return QIcon(pm)

def _draw_proj_twopoint_icon() -> QIcon:
    """Vector canvas for Two-Point Perspective icon (Vertically aligned cuts)."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    ink = _get_theme_ink()
    
    painter.setPen(QPen(ink, 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPolygon(QPolygonF([QPointF(24.0, 44.0), QPointF(4.0, 36.0), QPointF(4.0, 16.0), QPointF(24.0, 4.0)]))
    painter.drawPolygon(QPolygonF([QPointF(24.0, 4.0), QPointF(44.0, 16.0), QPointF(44.0, 36.0), QPointF(24.0, 44.0)]))
    painter.setPen(QPen(ink, 2.0, Qt.PenStyle.DashLine))
    painter.drawLine(QPointF(4.0, 28.0), QPointF(44.0, 28.0))
    painter.end()
    return QIcon(pm)

def _draw_zoom_combo_icon() -> QIcon:
    """Vector canvas for Smart Zoom icon (Enlarging glass with crosshair borders)."""
    pm = QPixmap(48, 48)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    ink = _get_theme_ink()
    
    painter.setPen(QPen(QColor("#000000") if theme.saved_theme() == theme.LIGHT else ink, 4.2))
    painter.setBrush(QColor("#F5B88C"))
    painter.drawEllipse(QPointF(20.5, 20.9), 13.0, 13.0)
    
    painter.setPen(QPen(QColor("#000000") if theme.saved_theme() == theme.LIGHT else ink, 5.6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    painter.drawLine(QPointF(29.4, 29.4), QPointF(40.3, 40.3))
    
    painter.setPen(QPen(QColor("#F58634"), 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    
    path = QPainterPath()
    path.moveTo(4.0, 16.0); path.lineTo(4.0, 4.0); path.lineTo(16.0, 4.0); painter.drawPath(path)
    path = QPainterPath()
    path.moveTo(44.0, 16.0); path.lineTo(44.0, 4.0); path.lineTo(32.0, 4.0); painter.drawPath(path)
    path = QPainterPath()
    path.moveTo(4.0, 32.0); path.lineTo(4.0, 44.0); path.lineTo(16.0, 44.0); painter.drawPath(path)
    path = QPainterPath()
    path.moveTo(44.0, 32.0); path.lineTo(44.0, 44.0); path.lineTo(32.0, 44.0); painter.drawPath(path)
    
    painter.end()
    return QIcon(pm)
def setup(app) -> None:
    window = getattr(app, "window", None)
    if not window or not hasattr(window, "menuBar"): return

    # TOOLBAR 1: Standard Views Container with embedded factory i18n
    views_toolbar = QToolBar(tr("Standard Views 2"), window)
    views_toolbar.setObjectName("StandardViews-2 Toolbar")

    home_action = QAction(tr("Isometric View"), views_toolbar)
    home_action.setToolTip(f"{tr('Isometric View')}\n{tr('Look at the model from a corner above, at the same angle to the three axes.')}")
    home_action.setIcon(_draw_iso_icon())
    home_action.triggered.connect(lambda: trigger_standard_isometric(app))
    views_toolbar.addAction(home_action)
    views_toolbar.addSeparator()

    # Enforced 100% accurate factory descriptions from views/main_window.py
    views_config = [
        ("Top View", _draw_top_icon, "top", "Look straight down on the model, in plan."),
        ("Front View", _draw_front_icon, "front", "Look at the model from the front."),
        ("Right View", _draw_right_icon, "right", "Look at the model from the right."),
        ("Left View", _draw_left_icon, "left", "Look at the model from the left."),
        ("Back View", _draw_back_icon, "back", "Look at the model from the back."),
        ("Bottom View", _draw_bottom_icon, "bottom", "Look at the model from below."),
    ]
    actions_map = {}
    for label, draw_func, view_name, core_tip in views_config:
        action = QAction(tr(label), views_toolbar)
        action.setToolTip(f"{tr(label)} ({tr('Parallel Projection')})\n{tr(core_tip)}")
        action.setIcon(draw_func())
        action.triggered.connect(lambda _, v=view_name: trigger_camera_view(app, v))
        views_toolbar.addAction(action)
        actions_map[view_name] = action
    views_toolbar.addSeparator()

    proj_cycle_action = QAction(tr("Camera Projection Mode"), views_toolbar)
    proj_cycle_action.setToolTip(f"{tr('Cycle Projection')}: {tr('Parallel')} -> {tr('Perspective')} -> {tr('2-Point Perspective')}")
    proj_cycle_action.setIcon(_draw_proj_perspective_icon())
    proj_cycle_action.triggered.connect(lambda: cycle_projection_modes(app))
    views_toolbar.addAction(proj_cycle_action)
    views_toolbar.addSeparator()
    views_toolbar.proj_cycle_action = proj_cycle_action

    zoom_combo_action = QAction(tr("Smart Zoom"), views_toolbar)
    zoom_combo_action.setToolTip(f"{tr('Toggle: Zoom Selected or Zoom Extents (if nothing is selected)')}\n{tr('Frame the whole model in the view.')}")
    zoom_combo_action.setIcon(_draw_zoom_combo_icon())
    zoom_combo_action.triggered.connect(lambda: trigger_smart_zoom_combo(app, window))
    views_toolbar.addAction(zoom_combo_action)
    views_toolbar.zoom_combo_action = zoom_combo_action

    # TOOLBAR 2: Standalone Theme Control Container
    theme_toolbar = QToolBar(tr("Theme Control"), window)
    theme_toolbar.setObjectName("Theme Toggler Toolbar")

    theme_action = QAction(tr("Toggle Theme Mode"), theme_toolbar)
    theme_action.setToolTip(f"{tr('Toggle Theme Mode')}\n{tr('Switch entire interface between Light and Dark modes natively')}")
    theme_action.setIcon(_draw_theme_squares_icon())
    theme_action.triggered.connect(lambda: toggle_global_preferences_theme(window))
    theme_toolbar.addAction(theme_action)

    views_toolbar.actions_map = actions_map
    views_toolbar.home_action = home_action
    views_toolbar.last_proj_state = None
    views_toolbar.last_theme_state = None

    def draw_ui_sync(viewport, painter):
        try:
            cam = viewport.camera if hasattr(viewport, "camera") else None
            if not cam: return
            is_dark_sync = theme.saved_theme() == theme.DARK
            is_persp = getattr(cam, "perspective", True)
            is_2pp = getattr(cam, "two_point", False)
            
            if is_persp and is_2pp:
                current_svg = "2pp_on.svg"
                active_proj_icon = _draw_proj_twopoint_icon()
            elif is_persp:
                current_svg = "perspective_on.svg"
                active_proj_icon = _draw_proj_perspective_icon()
            else:
                current_svg = "perspective_off.svg"
                active_proj_icon = _draw_proj_parallel_icon()
                
            if (views_toolbar.last_proj_state != current_svg) or (views_toolbar.last_theme_state != is_dark_sync):
                views_toolbar.last_proj_state = current_svg
                views_toolbar.last_theme_state = is_dark_sync
                
                views_toolbar.proj_cycle_action.setIcon(active_proj_icon)
                views_toolbar.home_action.setIcon(_draw_iso_icon())
                theme_action.setIcon(_draw_theme_squares_icon())
                views_toolbar.zoom_combo_action.setIcon(_draw_zoom_combo_icon())
                views_toolbar.actions_map["top"].setIcon(_draw_top_icon())
                views_toolbar.actions_map["front"].setIcon(_draw_front_icon())
                views_toolbar.actions_map["right"].setIcon(_draw_right_icon())
                views_toolbar.actions_map["left"].setIcon(_draw_left_icon())
                views_toolbar.actions_map["back"].setIcon(_draw_back_icon())
                views_toolbar.actions_map["bottom"].setIcon(_draw_bottom_icon())
        except Exception: pass

    app.add_overlay(draw_ui_sync)
    window.addToolBar(views_toolbar)
    window.addToolBar(theme_toolbar)

def toggle_global_preferences_theme(window) -> None:
    try:
        q_app = QApplication.instance()
        if not q_app: return
        current_mode = theme.saved_theme()
        next_mode = theme.LIGHT if current_mode == theme.DARK else theme.DARK
        theme.save_theme(next_mode)
        theme.apply_theme(q_app, next_mode)
        if hasattr(window, "_refresh_toolbar_icons"):
            window._refresh_toolbar_icons()
        q_app.processEvents()
        window.update()
    except Exception as e: print(f"Theme Toggler Error: {e}")

def cycle_projection_modes(app) -> None:
    try:
        if not app.viewport or not app.viewport.camera: return
        cam = app.viewport.camera
        is_persp = getattr(cam, "perspective", True)
        is_2pp = getattr(cam, "two_point", False)
        
        # Safe official sequence matching core shortcut and trigger pipelines
        if not is_persp:
            if hasattr(cam, "toggle_projection"):
                cam.toggle_projection()
        elif is_persp and not is_2pp:
            if hasattr(cam, "toggle_two_point"):
                cam.toggle_two_point()
        else:
            if hasattr(cam, "toggle_projection"):
                cam.toggle_projection()
                
        if hasattr(app.viewport, "_sync_projection"):
            app.viewport._sync_projection()
            
        app.viewport.update()
    except Exception as e: 
        print(f"Cycle Projection Modes Official Command Error: {e}")

def trigger_standard_isometric(app) -> None:
    try:
        vp = app.viewport
        if vp and hasattr(vp, "camera"):
            vp.camera.yaw = math.radians(-45.0)
            vp.camera.pitch = math.radians(30.0)
            vp.camera.perspective = True  
            vp.update()
    except Exception as e: print(f"Isometric View Error: {e}")

def trigger_camera_view(app, target_view: str) -> None:
    try:
        vp = app.viewport
        if vp and hasattr(vp, "camera"):
            vp.camera.set_view(target_view)
            vp.camera.perspective = False 
            vp.update()
    except Exception as e: print(f"Camera View Error: {e}")

def trigger_smart_zoom_combo(app, window) -> None:
    try:
        vp = app.viewport
        if not vp: return
        has_selection = False
        if hasattr(vp, "scene") and hasattr(vp.scene, "selection"):
            has_selection = len(vp.scene.selection) > 0
            
        if has_selection and hasattr(window, "_act_zoom_selection"):
            window._act_zoom_selection.trigger()
        elif hasattr(window, "_act_zoom_extents"):
            window._act_zoom_extents.trigger()
            
        vp.update()
    except Exception as e: 
        print(f"Smart Zoom Native Trigger Error: {e}")
