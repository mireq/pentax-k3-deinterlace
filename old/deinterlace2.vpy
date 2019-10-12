import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvs
import os
core = vs.get_core()
clip = core.ffms2.Source(source='/home/mirec/stm32-video/IMGP6624.MOV')
#clip = core.std.DeleteFrames(clip, range(0, 120, 2))

clip = core.std.AssumeFPS(clip, fpsnum=60000, fpsden=1001)
#clip = core.std.AssumeTFF(clip)
#clip = core.std.SeparateFields(clip, tff=True)
#clip = haf.Deblock_QED(clip)
#clip = haf.Weave(clip, tff=True)
#clip = mvs.AssumeTFF(clip)

clip = haf.QTGMC(Input=clip, Preset="Fast", TFF=False)
#clip = core.std.AssumeFPS(clip, fpsnum=60000, fpsden=1001)
clip.set_output()
