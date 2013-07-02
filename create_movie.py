#! /usr/bin/env python
#-*- encoding:utf-8 -*-

#import os.path
from os import path
from unicodedata import normalize
from subprocess import Popen, PIPE, call
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from PIL import Image, ImageFont, ImageDraw

# ffmpegのPATH
FFMPEG_PATH = "/usr/local/bin/ffmpeg"

# ファイル出力するPATH
FLV_SAVE_PATH = os.getenv("PATH")

class Make_file:
    
    def __init__(self, names, output_dir):
        self.names = names
        self.output_dir = output_dir

    def get_music_info(self):
        audios = []
        for name in self.names:
            audio = MP3(name, ID3=EasyID3)
            audio["length"] = str(audio.info.length)
            # 画像作成のために正規化形式 C に変換
            name = normalize("NFC", name)
            name = path.basename(name)
            name, ext = path.splitext(name)
            if "title" not in audio:
                #audio["title"] = ''.join(name.split('.')[:-1])
                audio["title"] = name
            audios.append(audio)

        #return audios
        self.audios = audios

    # 画像作成
    def make_jpg(self):
        width, height = (640,360)
        FONT_PATH = 'HGRME.ttc'
        font_size = 24
        font = ImageFont.truetype(FONT_PATH, font_size, encoding='utf-8')
        for audio in self.audios:
            text = audio["title"][0]
            size = font.getsize(text)
            img = Image.new('RGB', (width, height), 'black')
            draw = ImageDraw.Draw(img)
            w, h = font.getsize(text)
            draw.text(((width-w)/2,(height-h)/2), text, font=font, fill="white")
            text = text + ".jpg"
            img.save(text, "JPEG")

    # 画像と音楽をひとつずつ動画に変換
    def convert2mpg(self):
        """
        ffmpeg -i "sample.mp3" -loop 1 -f image2 -i "sample.png" -vcodec mpeg1video -b 50k -ab 256k -shortest "sample.mpg"
        """
        #for name in self.names:
        for i in range(len(self.names)):
            name = self.names[i]
            name, ext = path.splitext(name)
            input_mp3 = name + '.mp3'
            input_img = name + '.jpg'
            #output_mpg = name + '.mpg'
            output_mpg = 'music%03d.mpg' % (i+1)
            commands = (FFMPEG_PATH, '-y', '-i', input_mp3,
                    '-loop', '1', '-f', 'image2', '-i', input_img,
                    '-vcodec', 'mpeg1video', '-b', '50k', '-ab', '128k',
                    '-shortest', output_mpg )

            p = Popen(commands, stdout=PIPE, stderr=PIPE)
            print p.stderr.read()


    # 動画を繋げてひとつのmpgに出力
    def create_mpg(self):
        """
        ffmpeg -i "concat:input1.mpg|input2.mpg" -c copy output.mpg
        """
        commands = [FFMPEG_PATH, '-y', '-i']
        concat = "concat:"
        for i in range(len(self.names)):
            name, ext = path.splitext(self.names[i])
            concat += "music%03d.mpg" % (i+1)
            if i is not len(self.names)-1:
                concat += "|"
            #else:
            #    concat += ""

        commands += [concat, '-c', 'copy', 'output.mpg']
        commands = tuple(commands)

        #print commands
        p = Popen(commands, stdout=PIPE, stderr=PIPE)
        print p.stderr.read()

    def mpg2mp4(self):
        """
        ffmpeg -i inputfile.mpg -f mp4 -acodec aac -vcodec mpeg4 -b 256k -ab 64k outputfile.mp4
        """
        output = self.output_dir + '/output.mp4'
        commands = (FFMPEG_PATH, '-y', '-i', 'output.mpg', '-f', 'mp4',
                    '-vcodec', 'mpeg4', '-b', '50k', '-ab', '128k',
                    '-acodec', 'libfaac',
                    output )

        p = Popen(commands, stdout=PIPE, stderr=PIPE)
        print p.stderr.read()



def main(names):
    movie = Make_file(names)
    movie.get_music_info()
    movie.make_jpg()
    movie.convert2mpg()
    movie.create_mpg()
    movie.mpg2mp4()

    return "Finished!"


#--------------------
# 直接実行時に使用されるブロック
#--------------------
if __name__ == '__main__':
    import sys, os

    #コマンドライン引数の確認
    if len(sys.argv) > 1:
        mname=[]
        [mname.append(i) for i in sys.argv[1:len(sys.argv)]]

        file_name=[]
        [file_name.append(path.basename(mname[i])) for i in range(len(mname))]

        print main(file_name)


    else:
        print "引数がありません。"


