import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvs
import os


def combine(n, f):
	if n % 2 == 0:
		frame = f[0].copy()
	else:
		frame = f[1].copy()
	return frame


core = vs.get_core()
clip = core.ffms2.Source(source=os.environ['VIDEO_SOURCE'])
clip = core.std.SelectEvery(clip=clip, cycle=2, offsets=1)
clip = core.resize.Bicubic(clip, format=vs.YUV444P10)
clip = core.std.SelectEvery(clip=clip, cycle=2, offsets=[0, 0, 1, 1])
clip_odd = core.std.CropAbs(clip, clip.width, clip.height - 2, 0, 1)
clip_even = core.std.CropAbs(clip, clip.width, clip.height - 2, 0, 2)
clip = core.std.ModifyFrame(clip=clip_odd, clips=[clip_even, clip_odd], selector=combine)
clip = core.std.AssumeFPS(clip, fpsnum=60000, fpsden=1001)
clip = haf.QTGMC(Input=clip, Preset="Slow", TFF=True)
clip = core.std.SelectEvery(clip=clip, cycle=2, offsets=0)
clip = core.std.AddBorders(clip=clip, bottom=2)
clip.set_output()
