import copy
import manim as m
import numpy as np
from country_data import CountryData
from typing import List


class Globe(CountryData):
    # 1. Get polygon for the entire globe (we need to scale everything correctly)
    # 2. Get polygon for the country

    def get_country_globe(self, iso_a3_codes: List) -> m.Polygon:
        countries = self.list_all_countries_iso_a3()
        # Get coords for all countries
        # globe_coords_list = self.get_multiple_country_geometries(countries)
        # globe_cords_dict = dict(zip(countries, globe_coords_list))
        globe_coords_scaled_list = self.get_multiple_country_geometries_scaled(
            countries
        )

        # Function to check if any elements in a nested list of arbitrary depth and length are equal to a given value
        # globe_cords_scaled_dict = dict(zip(countries, globe_coords_scaled_list))

        globe_coords = self.__compute_xy_scaled_geometries_from_scaled_coords(
            globe_coords=globe_coords_scaled_list
        )

        def filter_none(x):
            if type(x) not in [float, np.float64]:
                print(type(x), x)
                print("SAKFDJS:FSLKDFJASDK:FJSAD:K")

                # print(x)
                # print(type(x))
                # print(type(x) is list or np.ndarray)
                [filter_none(i) for i in x]

        filter_none(globe_coords)
        raise Exception

        # Build 3D coordinates
        def build_globe(li: List) -> List:
            if isinstance(li[0], list):
                return [build_globe(i) for i in li]
            if isinstance(li[0], float):
                # Update coordinates to map to globe and return
                return [
                    np.cos(li[1] * np.cos(li[0])),
                    np.cos(li[1]) * np.sin(li[0]),
                    np.sin(li[1]),
                ]

        three_d_globe_coords = build_globe(globe_coords)
        globe_polys = m.VDict()
        # Creating Polygon from requested countries
        for country in iso_a3_codes:
            # Getting polygon coordinates for the requested country
            country_coords = three_d_globe_coords
            if len(iso_a3_codes) > 1:
                country_coords = three_d_globe_coords[iso_a3_codes.index(country)]
            globe_polys[country] = m.Polygon(*country_coords, color=m.BLUE)

        return np.array(globe_polys)

    def __compute_xy_scaled_geometries_from_scaled_coords(
        self, globe_coords: List
    ) -> List:
        # Compute scaling factor by getting range of dimension with max variance
        max_axis = np.argmax(
            [
                self.get_max_along_axis(globe_coords, 0),
                self.get_max_along_axis(globe_coords, 1),
            ]
        )

        # Computing scaling factor
        # We know we are scaling for the dimension that has not been scaled, so need to swap the axis
        min_axis = max_axis == 0 if max_axis == 0 else 1
        scale_factor = self.get_max_along_axis(
            globe_coords, min_axis
        ) - self.get_min_along_axis(globe_coords, min_axis)

        # Scaling each min_axis coordinate
        globe_coords = self.__iterate_until_base_and_scale(
            globe_coords, scale_factor, min_axis
        )

        return globe_coords

    def __iterate_until_base_and_scale(
        ### THE NONES ARE BEING INSERTED HERE SOMEWHERE!!!!!
        ###### AAAAAAAHHHHHH!!!!😤😅
        self,
        li: List,
        scale_factor: float,
        min_axis: int,
    ) -> List:
        if type(li[0]) in [float, np.float64]:
            if any(li) is None:
                print(li)
                raise Exception
            return [li[0], li[min_axis] / scale_factor, li[2]]
        if isinstance(li[0], list):
            return [
                self.__iterate_until_base_and_scale(i, scale_factor, min_axis)
                for i in li
            ]
        # if isinstance(li[0], float):
        #     li[min_axis] = li[min_axis] / scale_factor
        #     return li
