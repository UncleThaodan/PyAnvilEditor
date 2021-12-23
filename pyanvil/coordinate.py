from abc import ABC, abstractmethod


class Coordinate(ABC):
    def __init__(self, x: int = 0, z: int = 0):
        super().__init__()
        self.x: int = x
        self.z: int = z

    def __hash__(self) -> int:
        return hash((self.x, self.z))

    @abstractmethod
    def to_absolute_coordinate(self) -> 'AbsoluteCoordinate':
        pass

    @abstractmethod
    def to_chunk_coordinate(self) -> 'ChunkCoordinate':
        pass

    @abstractmethod
    def to_region_coordinate(self) -> 'RegionCoordinate':
        pass


class AbsoluteCoordinate(Coordinate):
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        super().__init__(x=x, z=z)
        self.y: int = y

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def to_absolute_coordinate(self) -> 'AbsoluteCoordinate':
        return self

    def to_chunk_coordinate(self) -> 'ChunkCoordinate':
        return ChunkCoordinate(self.x // 16, self.z // 16)

    def to_region_coordinate(self) -> 'RegionCoordinate':
        return RegionCoordinate(self.x // (16 * 32), self.z // (16 * 32))


class ChunkCoordinate(Coordinate):
    def __init__(self, x: int = 0, z: int = 0):
        super().__init__(x=x, z=z)

    def __hash__(self) -> int:
        return hash((self.x, self.z))

    def to_absolute_coordinate(self) -> 'AbsoluteCoordinate':
        return AbsoluteCoordinate(x=self.x * 16, y=0, z=self.z * 16)

    def to_chunk_coordinate(self) -> 'ChunkCoordinate':
        return self

    def to_region_coordinate(self) -> 'RegionCoordinate':
        return RegionCoordinate(self.x // 32, self.z // 32)


class RelativeChunkCoordinate(ChunkCoordinate):
    def __init__(self, x: int = 0, z: int = 0):
        super().__init__(x=x, z=z)

    def __hash__(self) -> int:
        return hash((self.x, self.z))


class RegionCoordinate(Coordinate):
    def __init__(self, x: int = 0, z: int = 0):
        super().__init__(x=x, z=z)

    def __hash__(self) -> int:
        return hash((self.x, self.z))

    def to_absolute_coordinate(self) -> 'AbsoluteCoordinate':
        return AbsoluteCoordinate(x=self.x * 16 * 32, y=0, z=self.z * 16 * 32)

    def to_chunk_coordinate(self) -> 'ChunkCoordinate':
        return ChunkCoordinate(self.x * 32, self.z * 32)

    def to_region_coordinate(self) -> 'RegionCoordinate':
        return self

    def to_region_file_name(self) -> 'str':
        return f'r.{self.x}.{self.z}.mca'

    @staticmethod
    def from_region_file_name(file_name: str) -> 'RegionCoordinate':
        from pathlib import Path
        path: Path = Path(file_name)
        if not path.name.endswith('.mca'):
            raise Exception(f'File name {file_name} is not a valid region file')
        parts = path.stem.split('.')
        return RegionCoordinate(x=int(parts[1]), z=int(parts[2]))
