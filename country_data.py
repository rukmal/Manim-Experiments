from altitude import AltitudeInterpolator
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union, nearest_points
from typing import Callable, List
import json
import numpy as np
import requests


class CountryData:
    base_df: dict
    al: AltitudeInterpolator

    def __init__(self):
        self.base_df = json.loads(open("countries.geojson", "r").read())
        self.al = AltitudeInterpolator()

    def get_country_data(self, iso_a3: str) -> dict:
        for feature in self.base_df["features"]:
            if feature["properties"]["ISO_A3"] == iso_a3.upper():
                return feature
        return None

    def get_country_name(self, iso_a3: str) -> str:

        return self.get_country_data(iso_a3)["properties"]["ADMIN"]

    def list_all_countries_iso_a3(self) -> List:
        countries = []
        for feature in self.base_df["features"]:
            countries.append(feature["properties"]["ISO_A3"])
        return countries

    def get_country_geometry(self, iso_a3: str) -> List[List]:
        """Returns the geometry of the country as a list of list of coordinates,
        where each top-level list corresponds to an individual polygon of the country.

        Arguments:
            iso_a3 {str} -- ISO A3 country code.

        Returns:
            List[List] -- List of list of coordinates.
        """

        try:
            _ = self.get_country_data(iso_a3)["geometry"]["coordinates"][0][0][0][0]
            return [
                i[0] for i in self.get_country_data(iso_a3)["geometry"]["coordinates"]
            ]
        except TypeError:
            return [self.get_country_data(iso_a3)["geometry"]["coordinates"][0]]

    def get_country_geometry_scaled(
        self, iso_a3: str, add_z: bool = True
    ) -> List[List]:
        country_polys = self.get_country_geometry(iso_a3)
        return self.__compute_scaled_geometries_from_polys(country_polys, add_z=add_z)

    def get_multiple_country_geometries(self, iso_a3s: List):
        geometries = []
        for iso_a3 in iso_a3s:
            geometries.append(self.get_country_geometry(iso_a3))
        return geometries

    def get_multiple_country_geometries_scaled(self, iso_a3s: List, add_z: bool = True):
        geometries = self.get_multiple_country_geometries(iso_a3s)
        # Combining geometries to get unified scaled geoms
        combined_geoms = []
        [combined_geoms.extend(country_geom) for country_geom in geometries]
        # Computing scaled geometries for combined geoms
        scaled_geoms_combined = self.__compute_scaled_geometries_from_polys(
            combined_geoms, add_z=add_z
        )

        # Splitting scaled geoms into individual countries
        idx = 0
        scaled_geoms = []
        for i, _ in enumerate(iso_a3s):
            scaled_geoms.append(scaled_geoms_combined[idx : idx + len(geometries[i])])
            idx += len(geometries[i])

        return scaled_geoms

    def get_max_along_axis(self, data: List[List], axis: int) -> float:
        """Returns the maximum value along a given axis.

        Arguments:
            data {List[List]} -- List of list of coordinates.
            axis {int} -- Axis along which to compute the maximum.

        Returns:
            float -- Maximum value.
        """

        max_val = -1e10
        for poly in data:
            for coordinate in poly:
                if coordinate[axis] > max_val:
                    max_val = coordinate[axis]
        return max_val

    def get_min_along_axis(self, data: List[List], axis: int) -> float:
        """Returns the minimum value along a given axis.

        Arguments:
            data {List[List]} -- List of list of coordinates.
            axis {int} -- Axis along which to compute the minimum.

        Returns:
            float -- Minimum value.
        """

        min_val = 1e10
        for poly in data:
            for coordinate in poly:
                if coordinate[axis] < min_val:
                    min_val = coordinate[axis]
        return min_val

    def __compute_scaled_geometries_from_polys(
        self, country_polys: List, add_z: bool = True
    ) -> List[List[List]]:
        # Compute scaling factor by getting range of dimension with max variance
        max_axis = np.argmax(
            [
                self.get_max_along_axis(country_polys, 0),
                self.get_max_along_axis(country_polys, 1),
            ]
        )
        scale_factor = self.get_max_along_axis(
            country_polys, max_axis
        ) - self.get_min_along_axis(country_polys, max_axis)
        min_values = [
            self.get_min_along_axis(country_polys, 0),
            self.get_min_along_axis(country_polys, 1),
        ]

        # Scaling each point and conditionally adding z coordinate
        scaled_polys = []
        for poly in country_polys:
            scaled_poly = []
            scaled_points = list((np.array(poly) - np.array(min_values)) / scale_factor)
            for coordinate in scaled_points:
                if len(coordinate) < 3 and add_z:
                    c = np.append(coordinate, 0)
                else:
                    c = coordinate
                scaled_poly.append(c)
            scaled_polys.append(scaled_poly)

        return [list(i) for i in scaled_polys]

    def get_longitude_and_latitude_from_scaled_xy(
        self, iso_a3: str, x: float, y: float
    ) -> List[float]:
        # Need scaling factor of the country
        # Need lower bounds for latitude and longitude of the country
        # Return [min_longitude + x * scaling_factor, min_latitude + y * scaling_factor]
        # Get country geometry
        country_polys = self.get_country_geometry(iso_a3)

        # Compute scaling factor by getting range of dimension with max variance
        max_axis = np.argmax(
            [
                self.get_max_along_axis(country_polys, 0),
                self.get_max_along_axis(country_polys, 1),
            ]
        )
        scale_factor = self.get_max_along_axis(
            country_polys, max_axis
        ) - self.get_min_along_axis(country_polys, max_axis)
        min_values = [
            self.get_min_along_axis(country_polys, 0),
            self.get_min_along_axis(country_polys, 1),
        ]

        # Compute longitude and latitude
        longitude = (x * scale_factor) + min_values[0]
        latitude = (y * scale_factor) + min_values[1]

        return [longitude, latitude]

    def build_uv_for_country(
        self, iso_a3: str, include_altitude: bool = True
    ) -> Callable:
        country_poly = self.get_country_polygon(iso_a3)

        # Defining uv map function
        def uv_map(u, v):
            point = Point(u, v)
            if not country_poly.contains(point):
                # Get closest point on polygon
                u, v = self.__get_nearest_point_on_polygon(country_poly, u, v)
            # Compute actual latitude and longitude for API call
            lon, lat = self.get_longitude_and_latitude_from_scaled_xy(iso_a3, u, v)
            if include_altitude:
                # Get altitude from altitude interpolator
                altitude = self.al.get_altitude(latitude=lat, longitude=lon)
                return np.array([lon, lat, altitude])
            else:
                return np.array([lon, lat, 0.0])

        return uv_map

    def get_country_polygon(self, iso_a3: str) -> Polygon:
        """Returns a polygon of the country.

        Arguments:
            iso_a3 {str} -- ISO A3 country code.

        Returns:
            Polygon -- Polygon of the country.
        """

        two_d_country = self.get_country_geometry_scaled(iso_a3, add_z=False)
        two_d_polygons = []
        for poly in two_d_country:
            two_d_polygons.append(Polygon(np.array(poly)))
        two_d_country_poly = unary_union(two_d_polygons)
        return two_d_country_poly

    def __get_nearest_point_on_polygon(
        self, polygon: Polygon, x: float, y: float
    ) -> List[float]:
        """Returns the nearest point on a polygon to a given point.

        Arguments:
            polygon {Polygon} -- Polygon.
            x {float} -- x coordinate of point.
            y {float} -- y coordinate of point.

        Returns:
            Point -- Nearest point on polygon.
        """

        return list(nearest_points(Point(x, y), polygon)[1].coords)[0]
