import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvs
import os

ignore_threshold=140
scene_change_percentage=15
dst_fps = 60


analParams = {
	'overlap': 0,
	'search': 3,
	'truemotion': True,
#        'chroma': True,
#        'blksize':16,
#        'searchparam':1
}
blockParams = {
	'thscd1': ignore_threshold,
	'thscd2': int(scene_change_percentage*255/100),
	'mode': 3,
}

import random

def combine(n, f):
	if n % 2 == 0:
		frame = f[0].copy()
	else:
		frame = f[1].copy()
	return frame


def set_frame_numbers(n, f):
	frame = f.copy()
	frame.props['FrameNumber'] = n
	return frame


core = vs.get_core()
clip = core.ffms2.Source(source=os.environ['VIDEO_SOURCE'])
clip = core.std.SelectEvery(clip=clip, cycle=2, offsets=1)
clip = core.std.AssumeFPS(clip, fpsnum=30000, fpsden=1001)
clip = core.std.SeparateFields(clip)
odd = core.std.SelectEvery(clip=clip, cycle=2, offsets=0)
even = core.std.SelectEvery(clip=clip, cycle=2, offsets=1)
sup_odd  = core.mv.Super(odd, pel=2)
sup_even  = core.mv.Super(even, pel=2)
bvec_odd = core.mv.Analyse(sup_odd, isb=True, **analParams)
fvec_odd = core.mv.Analyse(sup_odd, isb=False, **analParams)
bvec_even = core.mv.Analyse(sup_even, isb=True, **analParams)
fvec_even = core.mv.Analyse(sup_even, isb=False, **analParams)
clip_odd = core.mv.BlockFPS(odd, sup_odd, bvec_odd, fvec_odd,  num=60000, den=1001, **blockParams)
clip_even = core.mv.BlockFPS(even, sup_even, bvec_even, fvec_even,  num=60000, den=1001, **blockParams)

clip_odd = core.std.ModifyFrame(clip=clip_odd, clips=[clip_odd], selector=set_frame_numbers)
clip_odd = core.std.SelectEvery(clip=clip_odd, cycle=2, offsets=[0, 0, 1, 1])
clip_even = core.std.SelectEvery(clip=clip_even, cycle=2, offsets=[0, 0, 1, 1])
clip_odd = core.std.AssumeFPS(clip_odd, fpsnum=60000, fpsden=1001)
clip_even = core.std.AssumeFPS(clip_even, fpsnum=60000, fpsden=1001)
clip_even = core.std.DuplicateFrames(clip_even, [0, 0])
#clip_odd = core.std.DuplicateFrames(clip_odd, [0])
clip = core.std.ModifyFrame(clip=clip_even, clips=[clip_even, clip_odd], selector=combine)
clip = core.std.AssumeFPS(clip, fpsnum=60000, fpsden=1001)

clip = core.std.DoubleWeave(clip_odd, tff=False)
#clip = core.std.AssumeFPS(clip, fpsnum=60000, fpsden=1001)
#clip = core.std.Splice(clips=[clip_odd, clip_even])
#clip = mvs.AssumeTFF(clip)
clip = haf.QTGMC(Input=clip, Preset="Medium", TFF=True, FPSDivisor=2)
clip = core.std.SelectEvery(clip=clip, cycle=2, offsets=0)
clip = core.std.AssumeFPS(clip, fpsnum=60000, fpsden=1001)
clip.set_output()
