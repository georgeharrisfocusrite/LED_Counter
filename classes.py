import cv2
import imutils.contours

class Image:
    def __init__(self, image=None, image_path=None, channels=None, show=None, caption=None, thresh=170, erode_itr=2, dilate_itr=4, scale=1, blur=3, blob_size=500):

        if image is None:
            if image_path is None:
                self.image = None
            else:
                self.image = cv2.imread(image_path)
        else:
            self.image = image

        if channels is None:
            channels = 'BGR'
        self.channels = channels

        if show is None:
            show = False
        self.show = show

        if caption is None:
            caption = 'original image'
        self.caption = caption

        self.thresh=thresh
        self.scale=scale
        self.erode_itr=erode_itr
        self.dilate_itr=dilate_itr
        self.blur=blur
        self.blob_size=blob_size

    def resize(self, x_scale, y_scale):
        # resize image
        self.image = cv2.resize(self.image, None, fx=self.scale, fy=self.scale)

    @property
    def grayed(self):
        # convert to b&w
        return Image( image=cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY), caption='grayscale image', thresh=self.thresh, scale=self.scale, blur=self.blur, channels = 'gray' )

    @property
    def blurred(self):
        if self.blur % 2 == 0:
            self.blur += 1
        # apply gaussian blur
        return Image( cv2.GaussianBlur(self.image, (self.blur, self.blur), 0), caption='blurred image', thresh=self.thresh, scale=self.scale, blur=self.blur, channels = self.channels )

    @property
    def threshold(self):
        # apply brightness threshold
        thresh = cv2.threshold(self.image, self.thresh, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=self.erode_itr)
        thresh = cv2.dilate(thresh, None, iterations=self.dilate_itr)
        return thresh

    # TODO fix masked image being grayscale underneath
    @property
    def masked(self):
        # use thresh to mask original image
        return Image( cv2.bitwise_and(self.image, self.image, mask=self.threshold), caption='masked image', thresh=self.thresh, scale=self.scale, blur=self.blur, channels = self.channels )

    @property
    def countleds(self):
        # count LEDs
        cnts = cv2.findContours(self.threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        return len([cnt for cnt in imutils.grab_contours(cnts) if cv2.contourArea(cnt) > self.blob_size])