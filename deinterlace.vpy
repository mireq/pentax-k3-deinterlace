import numpy as np
import os
import vapoursynth as vs


def modify_frame(n, f):
	frame = f.copy()
	for plane in range(frame.format.num_planes):
		write_array = np.array(frame.get_write_array(plane), copy=False)
		write_array[:] = np.roll(write_array, 1, axis=0)
		write_array[0,:] = write_array[1,:]
		if n % 2 == 1:
			copy = write_array.copy()
			write_array[0::2,:] = copy[1::2,:]
			write_array[1::2,:] = copy[0::2,:]
	return frame


core = vs.get_core()
core.max_cache_size = 1024
clip = core.ffms2.Source(source=os.environ['VIDEO_SOURCE'])
clip = core.resize.Bicubic(clip, format=vs.YUV444P8)
clip = core.std.ModifyFrame(clip, clip, modify_frame)
clip = core.std.AssumeFPS(clip, fpsnum=60000, fpsden=1001)
clip = core.nnedi3.nnedi3(clip=clip, field=1, nsize=0, nns=2, qual=2, etype=1)
clip.set_output()
