import logging
from typing import Union
from pathlib import Path

from .components.region import Region
from .coordinate import AbsoluteCoordinate, ChunkCoordinate, RegionCoordinate
from .canvas import Canvas
from .components import Chunk, Block
from .utility.nbt import NBT
from .stream import InputStream
import gzip


class World:
    def __init__(self, world_folder, read=True, write=True):
        self.world_folder: Path = self.__resolve_world_folder(world_folder=world_folder)
        self.regions: dict[RegionCoordinate, Region] = dict()

        self.__level_dat_data = World.__read_level_file(self.world_folder)

    @staticmethod
    def __read_level_file(world_folder: Path):
        with open(world_folder / 'level.dat', 'r+b') as file:
            data = gzip.decompress(file.read())
            stream = InputStream(data)
            return NBT.parse_nbt(stream)

    def __resolve_world_folder(self, world_folder: Union[str, Path]) -> Path:
        folder = Path(world_folder)
        if not folder.is_dir():
            raise FileNotFoundError(f'No such folder \"{folder}\"')
        return folder

    def __enter__(self) -> 'World':
        return self

    def __exit__(self, typ, val, trace):
        if typ is None:
            self.close()

    def flush(self):
        self.close()
        self.regions: dict[RegionCoordinate, Region] = dict()

    def close(self):
        for region in self.regions.values():
            if region.is_dirty:
                region.save()

    def get_block(self, coordinate: AbsoluteCoordinate) -> Block:
        RegionCoordinate.to_region_file_name(coordinate.to_region_coordinate())
        chunk = self.get_chunk(coordinate.to_chunk_coordinate())
        return chunk.get_block(coordinate)

    def get_region(self, coord: RegionCoordinate):
        return self.regions.get(coord, self._load_region(coord))

    def get_chunk(self, coord: ChunkCoordinate) -> Chunk:
        region = self.get_region(coord.to_region_coordinate())
        return region.get_chunk(coord)

    def get_canvas(self):
        return Canvas(self)

    def _load_region(self, coord: RegionCoordinate):
        logging.debug(f'Region {coord} not in memory. Loading...')
        name = RegionCoordinate.to_region_file_name(coord)
        region = Region(self.world_folder / 'region' / name)
        self.regions[coord] = region
        logging.debug(f'Region {coord} loaded.')
        return region
