import unittest
import pyglet
import Objects


class TestTerrainUnit(unittest.TestCase):

    def test_terrain_width_height(self):

        for coord in Objects.terrain_obj.terrain_dict:

            cell = Objects.terrain_obj.terrain_dict[coord]

            self.assertEquals(cell.sprite.height, cell.unit_size * cell.sprite.scale)
            self.assertEquals(cell.sprite.width, cell.unit_size * cell.sprite.scale)

    def test_terrain_spacing(self):

        pass




if __name__ == '__main__':
    unittest.main()