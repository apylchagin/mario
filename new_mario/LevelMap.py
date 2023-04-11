#!/usr/bin/env python3

# Defines the rectangle block on the map
# as a type, start coordinates as x,y and
# dims as width and height
class LevelBlock:
    # Block type identified
    type = None
    x = 0
    y = 0
    width = 0
    height = 0

    # Constructor
    def __init__(self, atype ,ax, ay):
        self.type = atype
        self.x = ax
        self.y = ay
        self.width = 1
        self.height = 1

    # String conversion
    def __str__(self):
        return "(%c [%d, %d] %dx%d)" % (self.type, self.x, self.y, self.width, self.height)

# This class describes the level map. Every block on map
# represents by the LevelBlock with type and location.
class LevelMap:
    width = 0
    height = 0
    blocks = None

    # Constructor
    def __init__(self):
        pass

    # Convert to string
    def __str__(self):
        __result = "{%dx%d:" % (self.width, self.height)
        for block in self.blocks:
            __result += "[%s]" % (str(block))
        __result += "}"
        return __result

    # Function build the map out of the text file
    def loadFromFile(self, path):
        __result = None
        try:
            f = open(path, "rt")
            __lines = f.readlines()
            __result = self.loadFromString(__lines)
        except FileNotFoundError:
            print("Failed to open file %s" % (path))
        return __result

    # Function build the map out of the strings
    def loadFromString(self, lines):
        self.blocks = []
        lines = self.__chompLines(lines)
        if self.__calculateMapSize(lines):
            while True:
                __block = self.__findNext(lines)
                if __block[0] is None:
                    # Stop if no more blocks found
                    break
                # Store the block into the list
                # of found blocks
                self.blocks.append(__block[0])
                # Reassign the lines by the ones
                # there the data for the just extracted
                # block has removed
                lines = __block[1]
            return True
        return False

    # Check that all lines have the same length
    # and calculate the map sizes: width and height
    def __calculateMapSize(self, lines):
        __len = 0
        for line in lines:
            if __len == 0:
                __len = len(line)
            elif __len != len(line):
                return False
        self.width = __len
        self.height = len(lines)
        return True

    # Remove line endings
    def __chompLines(self, lines):
        __result = []
        for line in lines:
            __result.append(line.rstrip("\n\r\t"))
        return __result

    # Finds the next rectangular block. Return the pair
    # of the LevelBlock instance and new updated lines
    # where the block related data has removed.
    def __findNext(self, lines):
        __block = None
        # Find the very first not-empty type to indicate
        # start of the block and the length of the very
        # first line.
        for idx in range(self.height):
            for idx2 in range(self.width):
                if lines[idx][idx2] != ' ':
                    if __block is None:
                        # The block start has found, create the object
                        # to handle it
                        __block = LevelBlock(lines[idx][idx2], idx2, idx)
                    elif lines[idx][idx2] == __block.type:
                        # Keep counting the line
                        __block.width += 1
                    else:
                        # Another block has started
                        break
                elif __block is not None:
                    # The block was found and now we see
                    # empty space, i.e. the region outside
                    # the block
                    break
            if __block is not None:
                break

        # if there is a block we found need to check it.
        if __block is not None:
            # Try to extract the block from the __block.x/y point and
            # the width in __block.width, i.e. as the very first line
            for idx in range(__block.y + 1, self.height):
                if lines[idx][__block.x] != __block.type:
                    # The next line has no type at the first position
                    # thus, we've done
                    break
                # Scan entire line
                for idx2 in range(__block.x, __block.x + __block.width):
                    if lines[idx][idx2] != __block.type:
                        # The line must be __block.width length with
                        # the same type
                        __block = None
                        break
                if __block is None:
                    # Validation has failed
                    break
                # Count this line as valid
                __block.height += 1

        # Need to remove the found block from the lines
        if __block is not None:
            __wiper = ' ' * __block.width
            for idx in range(__block.y, __block.y + __block.height):
                # Replace the block's content with spaces
                lines[idx] = lines[idx][:__block.x] + __wiper + lines[idx][__block.x + __block.width:]
        return __block, lines


if __name__ == '__main__':
      map = LevelMap()
      map.loadFromFile("level1.map")
      print("Map is %d x %d" % (map.width, map.height))
      for block in map.blocks:
          print("-> block: %s" % (str(block)))

#levelmap 2,3
if __name__ == '__main__':
      map = LevelMap()
      map.loadFromFile("level2.map")
      print("Map is %d x %d" % (map.width, map.height))
      for block in map.blocks:
          print("-> block: %s" % (str(block)))
