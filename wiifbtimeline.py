#!/usr/bin/python
import Image, sys, os

kFB_COVER_SIZE = (851,315)
kWII_SLOT_GRID_SIZE = (4,2)

def main():
	if len(sys.argv) < 3:
		print 'usage: %s <output filename> <input thumbnails...>' % sys.argv[0]
		return

	print 'Creating cover photo from images: %s' % sys.argv[2:]
	img = create_cover(sys.argv[2:])

	print 'Saving generated cover photo as %s' % sys.argv[1]
	img.save(sys.argv[1])

# throws IOError if any files fail to open
def create_cover(thumbnail_filenames):
	backgroundImage = Image.open(os.path.join(sys.path[0], 'background.png'))
	foregroundImage = Image.open(os.path.join(sys.path[0], 'foreground.png'))

	if backgroundImage.size != kFB_COVER_SIZE:
		print 'warning: background image is not the right size for timeline covers.'
		print 'should be %s is %s' % (kFB_COVER_SIZE, backgroundImage.size)

	if foregroundImage.size != kFB_COVER_SIZE:
		print 'warning: foreground image is not the right size for timeline covers.'
		print 'should be %s is %s' % (kFB_COVER_SIZE, foregroundImage.size)

	grid_width = kWII_SLOT_GRID_SIZE[0]
	grid_height = kWII_SLOT_GRID_SIZE[1]

	tile_width = kFB_COVER_SIZE[0] / grid_width
	tile_height = kFB_COVER_SIZE[1] / grid_height

	newImage = Image.new('RGB', kFB_COVER_SIZE)

	newImage.paste(backgroundImage, (0,0))

	i = 0
	for y in range(grid_height):
		for x in range(grid_width):
			# skip bottom left slot
			if y == 1 and x == 0:
				continue
			if i < len(thumbnail_filenames):
				currTile = Image.new('RGB', (tile_width, tile_height))
				thumb = Image.open(thumbnail_filenames[i])
				thumb.thumbnail((tile_width, tile_height), Image.ANTIALIAS)
				region = (currTile.size[0]/2 - thumb.size[0]/2,
						currTile.size[1]/2 - thumb.size[1]/2)
				currTile.paste(thumb, region)
				newImage.paste(currTile, (x*tile_width, y*tile_height))

			i += 1

	newImage.paste(foregroundImage, (0,0), foregroundImage)

	return newImage

if __name__ == '__main__':
	main()
