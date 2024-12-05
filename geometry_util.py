from dataclasses import dataclass, field
import plotly.graph_objects as go
import random


@dataclass
class Cuboid:
    x_range_tuple: tuple
    y_range_tuple: tuple
    z_range_tuple: tuple
    x: list = field(default_factory=list)
    y: list = field(default_factory=list)
    z: list = field(default_factory=list)
    shape: go.Isosurface = None

    def get_volume(self) -> int:
        x_size = abs(self.x_range_tuple[1] - self.x_range_tuple[0]) + 1
        y_size = abs(self.y_range_tuple[1] - self.y_range_tuple[0]) + 1
        z_size = abs(self.z_range_tuple[1] - self.z_range_tuple[0]) + 1
        return x_size * y_size * z_size

    def overlaps(self, cuboid: 'Cuboid'):
        x_min, x_max = cuboid.x_range_tuple
        y_min, y_max = cuboid.y_range_tuple
        z_min, z_max = cuboid.z_range_tuple

        # -44 -> 5 :: -5 -> 47
        x_overlaps = x_min <= self.x_range_tuple[0] and x_max >= self.x_range_tuple[0] or \
                     x_min >= self.x_range_tuple[0] and x_min <= self.x_range_tuple[1]

        y_overlaps = y_min <= self.y_range_tuple[0] and y_max >= self.y_range_tuple[0] or \
                     y_min >= self.y_range_tuple[0] and y_min <= self.y_range_tuple[1]

        z_overlaps = z_min <= self.z_range_tuple[0] and z_max >= self.z_range_tuple[0] or \
                     z_min >= self.z_range_tuple[0] and z_min <= self.z_range_tuple[1]

        return x_overlaps and y_overlaps and z_overlaps

    def get_overlap_range(self, own_range, their_range):
        min, max = their_range
        overlap_range = None
        # own range envelops their range 0 -> 5 : 1 -> 3
        if min >= own_range[0] and max <= own_range[1]:
            overlap_range = (min, max)
        # their range envelops own range 1 -> 3 : 0 -> 5
        elif min <= own_range[0] and max >= own_range[1]:
            overlap_range = own_range
        # right overlap their range to own range  1 -> 3 : 2 -> 4
        elif own_range[0] <= min < own_range[1] <= max:
            overlap_range = (min, own_range[1])
        # left overlap their range to own range  2 -> 4 : 1 -> 3
        elif min <= own_range[0] < max <= own_range[1]:
            overlap_range = (own_range[0], max)

        return overlap_range

    def get_overlap_cuboid(self, cuboid: 'Cuboid'):
        x_overlap_range = self.get_overlap_range(cuboid.x_range_tuple, self.x_range_tuple)
        y_overlap_range = self.get_overlap_range(cuboid.y_range_tuple, self.y_range_tuple)
        z_overlap_range = self.get_overlap_range(cuboid.z_range_tuple, self.z_range_tuple)
        return Cuboid(cuboid.action, x_overlap_range, y_overlap_range, z_overlap_range)

    def three_d(self, fill_value=1):
        x_min, x_max = self.x_range_tuple
        y_min, y_max = self.y_range_tuple
        z_min, z_max = self.z_range_tuple

        # The
        # octants
        # are: | (+x, +y, +z) | (-x, +y, +z) | (+x, +y, -z) | (-x, +y, -z) | (+x, -y, +z) | (-x, -y, +z) | (
        # +x, -y, -z) | (-x, -y, -z) |

        self.x = [x_max, x_min, x_max, x_min, x_max, x_min, x_max, x_min]
        self.y = [y_max, y_max, y_max, y_max, y_min, y_min, y_min, y_min]
        self.z = [z_max, z_max, z_min, z_min, z_max, z_max, z_min, z_min]

        self.shape = go.Isosurface(
                x=self.x,
                y=self.y,
                z=self.z,
                value=[fill_value for _ in range(len(self.x))],
                opacity=.4,
                isomin=0,
                isomax=5,
                visible=True)

    def split_cuboid(self, overlap: 'Cuboid'):
        splits = []

        z_min, z_max = self.z_range_tuple
        # Only create new cuboid is dimension does not dissapear in other cube
        if z_min < overlap.z_range_tuple[0] or z_max > overlap.z_range_tuple[1]:
            z_min = overlap.z_range_tuple[1] + 1 if overlap.z_range_tuple[1] < z_max else z_min
            z_max = overlap.z_range_tuple[0] - 1 if overlap.z_range_tuple[0] > z_min else z_max
            cub_z = Cuboid(overlap.x_range_tuple, overlap.y_range_tuple, (z_min, z_max))
            splits.append(cub_z)

        x_min, x_max = self.x_range_tuple
        if x_min < overlap.x_range_tuple[0] or x_max > overlap.x_range_tuple[1]:
            x_min = overlap.x_range_tuple[1] + 1 if overlap.x_range_tuple[1] < x_max else x_min
            x_max = overlap.x_range_tuple[0] - 1 if overlap.x_range_tuple[0] > x_min else x_max
            cub_x = Cuboid((x_min, x_max), overlap.y_range_tuple, self.z_range_tuple)
            splits.append(cub_x)

        y_min, y_max = self.y_range_tuple
        if y_min < overlap.y_range_tuple[0] or y_max > overlap.y_range_tuple[1]:
            y_min = overlap.y_range_tuple[1] + 1 if overlap.y_range_tuple[1] < y_max else y_min
            y_max = overlap.y_range_tuple[0] - 1 if overlap.y_range_tuple[0] > y_min else y_max
            cub_y = Cuboid(self.x_range_tuple, (y_min, y_max), self.z_range_tuple)
            splits.append(cub_y)

        return splits

    def split_nested_cuboid(self, nested: 'Cuboid'):
        sub_x_range = self.x_range_tuple[0], nested.x_range_tuple[1]
        sub_y_range = self.y_range_tuple[0], nested.y_range_tuple[1]
        sub_z_range = self.z_range_tuple[0], nested.z_range_tuple[1]

        sub_cuboid = Cuboid(sub_x_range, sub_y_range, sub_z_range)
        outer_cubs = self.split_cuboid(sub_cuboid)
        inner_cubs = sub_cuboid.split_cuboid(nested)

        return outer_cubs + inner_cubs

    def is_nested_in(self, cuboid: 'Cuboid'):
        x_min, x_max = self.x_range_tuple
        y_min, y_max = self.y_range_tuple
        z_min, z_max = self.z_range_tuple

        nested_x = x_min >= cuboid.x_range_tuple[0] and x_max <= cuboid.x_range_tuple[1]
        nested_y = y_min >= cuboid.y_range_tuple[0] and y_max <= cuboid.y_range_tuple[1]
        nested_z = z_min >= cuboid.z_range_tuple[0] and z_max <= cuboid.z_range_tuple[1]

        return nested_x and nested_y and nested_z
