from PIL import Image,ImageFont,ImageDraw
import os

class Imagehanler:
    

    logo_im = Image.open('./image/t_pic1.jpg')
    im = Image.open('./image/pic1.webp')
    
    def resize_image(self):
        new_logo = logo_im.resize((41,60), Image.ANTIALIAS)
        new_logo.save('./image/new_logo.png')
        logo_im = new_logo
        print(logo_im.size)
    
    def image_paste_logo(self):
        im.paste(logo_im, (x, y), mask=logo_im)
        im.save('./image/t_pic1.png')

if __name__ == '__main__':
    imagehandler = Imagehanler()
    #imagehandler.resize_image()
    
    title = 'Реком\nенда'
    font = ImageFont.truetype(os.path.join('/Users/liuyang/mi/i18n_cms/font', "dk-lantinggboutside.ttf"), int(42*1.5))
    draw = ImageDraw.Draw(Imagehanler.im)
    draw.text((0,0),title,font=font)
    Imagehanler.im.save('./image/title.jpg')
