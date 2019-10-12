import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvs
import os
core = vs.get_core()
clip = core.ffms2.Source(source=os.environ['VIDEO_SOURCE'])
clip = core.std.SelectEvery(clip=clip, cycle=2, offsets=1)
clip = core.std.AssumeFPS(clip, fpsnum=30000, fpsden=1001)
#clip = mvs.AssumeTFF(clip)
clip = haf.QTGMC(Input=clip, Preset="Medium", TFF=True)
clip.set_output()
