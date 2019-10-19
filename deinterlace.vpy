import havsfunc as haf
import numpy as np
import os
import vapoursynth as vs


def modify_frame(n, f):
	frame = f.copy()

	for plane in range(frame.format.num_planes):
		write_array = np.array(frame.get_write_array(plane), copy=False)

		# Fix extra line on every second frame
		if n % 2 == 1:
			write_array[:] = np.roll(write_array, 1, axis=0)
			write_array[0,:] = write_array[1,:]

		# Double height frame
		copy = write_array.copy()[0:write_array.shape[0]//2,:] # Copy top half of frame
		write_array[0::2,:] = copy # Assign to odd and even lines
		write_array[1::2,:] = copy

	return frame


core = vs.get_core()
core.max_cache_size = 1024
clip = core.ffms2.Source(source=os.environ['VIDEO_SOURCE'])
clip = core.std.SelectEvery(clip=clip, cycle=2, offsets=0)
clip = core.std.AddBorders(clip=clip, bottom=clip.height)
clip = core.std.SeparateFields(clip)
clip = core.std.ModifyFrame(clip, clip, modify_frame)

#clip = core.nnedi3.nnedi3(clip=clip, field=0, nsize=0, nns=2, qual=2, etype=1)
#clip = haf.QTGMC(Input=clip, Preset="Placebo", TFF=True, FPSDivisor=2, Lossless=0)
clip = haf.QTGMC(
	Input=clip,
	Preset="Faster",
	TFF=True,
	FPSDivisor=2,
	EdiMode='nnedi3',
	NNSize=0,
	NNeurons=2,
	EdiMaxD=8,
	Sharpness=0.5,
	SMode=2,
	SLMode=1,
	SLRad=3,
	Sbb=3,
	TR0=2,
	TR1=2,
	TR2=3,
	Rep0=4,
	Rep2=4,
)
clip.set_output()
