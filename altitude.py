from math import floor
from PIL import Image
from typing import Dict, List
import os


class AltitudeInterpolator:
    topography_maps: Dict[str, Image.Image]
    scaling_altitude_m: float = 8848.95  # Everest altitude
    scaling_altitude_ft: int = 29032
    tile_dim = 10800
    aspect = 90 / tile_dim
    size_deg = 90
    x_tile_idx = ["A", "B", "C", "D"]
    y_tile_idx = ["1", "2"]

    def __init__(self):
        # Override PIL flag to import large image
        Image.MAX_IMAGE_PIXELS = None
        self.topography_maps = {}

    def get_altitude(
        self, latitude: float, longitude: float, scaled: str = None
    ) -> float:
        assert (
            longitude <= 180
            and longitude >= -180
            and latitude <= 90
            and latitude >= -90
        )
        assert scaled in ["ft", "m", None]
        # Get tile and xy coordinates
        tile_x_y = self.get_tile_coords_from_lat_lon(latitude, longitude)
        # Get brightness value at pixel and scale
        brightness = self.get_pixel_value_from_tile(tile_x_y) / 255
        if scaled == "ft":
            return brightness * self.scaling_altitude_ft
        elif scaled == "m":
            return brightness * self.scaling_altitude_m
        else:
            return brightness

    def add_tile_to_cache(self, tile: str):
        self.topography_maps[tile] = Image.open(
            os.path.join("topography", tile + ".tiff")
        )

    def get_tile_coords_from_lat_lon(self, latitude: float, longitude: float) -> List:
        x_tile_idx = self.x_tile_idx[floor((longitude + 180) / self.size_deg)]
        y_tile_idx = self.y_tile_idx[
            len(self.y_tile_idx) - floor((latitude + 90) / self.size_deg) - 1
        ]
        return [
            x_tile_idx + y_tile_idx,
            int(((longitude + 180) % self.size_deg) / self.size_deg * self.tile_dim),
            self.tile_dim
            - int(((latitude + 90) % self.size_deg) / self.size_deg * self.tile_dim),
        ]

    def get_pixel_value_from_tile(self, tile_x_y: List) -> float:
        if tile_x_y[0] not in self.topography_maps:
            self.add_tile_to_cache(tile_x_y[0])
        return self.topography_maps[tile_x_y[0]].getpixel((tile_x_y[1], tile_x_y[2]))
