import glo
from VirtualScene.alive_scene import AliveScene


def main():
    # 初始化全局变量
    glo.init()
    alive_scene = AliveScene()
    alive_scene.run()


main()

