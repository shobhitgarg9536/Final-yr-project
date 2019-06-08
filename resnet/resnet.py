import numpy as np
from helpers import *
from keras.layers import *
from keras.models import Model
import tensorflow as tf
from tqdm import tqdm
import cv2

OBJ_THRESHOLD = 0.6
NMS_THRESHOLD = 0.5


IMAGE_H, IMAGE_W = 416, 416
GRID_H,  GRID_W  = 13 , 13
BOX = 5
CLASS = 80

def create_model():

    # the function to implement the organization layer
    def space_to_depth_x2(x):
        return tf.space_to_depth(x, block_size=2)

    # Define input
    x_input = Input([IMAGE_H, IMAGE_W, 3])

    
    x = Conv2D(32, (3, 3), strides=(1, 1), padding='same', name='conv_1', use_bias=False)(x_input)
    x = BatchNormalization(name='norm_1')(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    
    x = Conv2D(64, (3, 3), strides=(1, 1), padding='same', name='conv_2', use_bias=False)(x)
    x = BatchNormalization(name='norm_2')(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    
    x = Conv2D(128, (3, 3), strides=(1, 1), padding='same', name='conv_3', use_bias=False)(x)
    x = BatchNormalization(name='norm_3')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(64, (1, 1), strides=(1, 1), padding='same', name='conv_4', use_bias=False)(x)
    x = BatchNormalization(name='norm_4')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(128, (3, 3), strides=(1, 1), padding='same', name='conv_5', use_bias=False)(x)
    x = BatchNormalization(name='norm_5')(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    
    x = Conv2D(256, (3, 3), strides=(1, 1), padding='same', name='conv_6', use_bias=False)(x)
    x = BatchNormalization(name='norm_6')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(128, (1, 1), strides=(1, 1), padding='same', name='conv_7', use_bias=False)(x)
    x = BatchNormalization(name='norm_7')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(256, (3, 3), strides=(1, 1), padding='same', name='conv_8', use_bias=False)(x)
    x = BatchNormalization(name='norm_8')(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    
    x = Conv2D(512, (3, 3), strides=(1, 1), padding='same', name='conv_9', use_bias=False)(x)
    x = BatchNormalization(name='norm_9')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(256, (1, 1), strides=(1, 1), padding='same', name='conv_10', use_bias=False)(x)
    x = BatchNormalization(name='norm_10')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(512, (3, 3), strides=(1, 1), padding='same', name='conv_11', use_bias=False)(x)
    x = BatchNormalization(name='norm_11')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(256, (1, 1), strides=(1, 1), padding='same', name='conv_12', use_bias=False)(x)
    x = BatchNormalization(name='norm_12')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(512, (3, 3), strides=(1, 1), padding='same', name='conv_13', use_bias=False)(x)
    x = BatchNormalization(name='norm_13')(x)
    x = LeakyReLU(alpha=0.1)(x)

    skip_connection = x

    x = MaxPooling2D(pool_size=(2, 2))(x)

    
    x = Conv2D(1024, (3, 3), strides=(1, 1), padding='same', name='conv_14', use_bias=False)(x)
    x = BatchNormalization(name='norm_14')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(512, (1, 1), strides=(1, 1), padding='same', name='conv_15', use_bias=False)(x)
    x = BatchNormalization(name='norm_15')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(1024, (3, 3), strides=(1, 1), padding='same', name='conv_16', use_bias=False)(x)
    x = BatchNormalization(name='norm_16')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(512, (1, 1), strides=(1, 1), padding='same', name='conv_17', use_bias=False)(x)
    x = BatchNormalization(name='norm_17')(x)
    x = LeakyReLU(alpha=0.1)(x)

   
    x = Conv2D(1024, (3, 3), strides=(1, 1), padding='same', name='conv_18', use_bias=False)(x)
    x = BatchNormalization(name='norm_18')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(1024, (3, 3), strides=(1, 1), padding='same', name='conv_19', use_bias=False)(x)
    x = BatchNormalization(name='norm_19')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(1024, (3, 3), strides=(1, 1), padding='same', name='conv_20', use_bias=False)(x)
    x = BatchNormalization(name='norm_20')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    skip_connection = Conv2D(64, (1, 1), strides=(1, 1), padding='same', name='conv_21', use_bias=False)(
        skip_connection)
    skip_connection = BatchNormalization(name='norm_21')(skip_connection)
    skip_connection = LeakyReLU(alpha=0.1)(skip_connection)
    skip_connection = Lambda(space_to_depth_x2)(skip_connection)

    x = concatenate([skip_connection, x])

    
    x = Conv2D(1024, (3, 3), strides=(1, 1), padding='same', name='conv_22', use_bias=False)(x)
    x = BatchNormalization(name='norm_22')(x)
    x = LeakyReLU(alpha=0.1)(x)

    
    x = Conv2D(BOX * (4 + 1 + CLASS), (1, 1), strides=(1, 1), padding='same', name='conv_23')(x)


    output = Reshape([GRID_H, GRID_W, BOX, 4 + 1 + CLASS])(x)

    model = Model(x_input, output)

    print('Model created.')

    return model


# Create model and load weights
resnet = create_model()
load_weights(resnet, 'resnet.weights')
resnet.summary()


# All resnet actions from input to output
def make_resnet(original_image):
    input_image = cv2.resize(original_image, (IMAGE_H, IMAGE_W)) / 255.
    input_image = input_image[:, :, ::-1]
    input_image = np.expand_dims(input_image, 0)
    resnet_output = np.squeeze(resnet.predict(input_image))
    boxes = filter_boxes(resnet_output, OBJ_THRESHOLD)
    boxes = non_max_suppress(boxes, NMS_THRESHOLD)
    colours = generate_colors(LABELS)
    output_image = draw_boxes(original_image, boxes, LABELS, colours)

    return output_image


# Objects detection from image
def resnet_image(image_path):

    original_image = cv2.imread(image_path)
    image = make_resnet(original_image)
    cv2.imshow('frame', image)


# Objects detection from video
def resnet_video(video_path, faster_times=1):
    video_out = '/'.join(video_path.split('/')[:-1]) + '/out_' + video_path.split('/')[-1]
    video_reader = cv2.VideoCapture(video_path)
    nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = video_reader.get(cv2.CAP_PROP_FPS)
    video_writer = cv2.VideoWriter(video_out, cv2.VideoWriter_fourcc(*'XVID'),
                                   fps * faster_times, (frame_w, frame_h))
    for _ in tqdm(range(nb_frames)):

        ret, original_image = video_reader.read()
        image = make_resnet(original_image)
        video_writer.write(np.uint8(image))

    video_reader.release()
    video_writer.release()



def resnet_live(mirror=True):

    cap = cv2.VideoCapture(0)

    while(True):

        ret, frame = cap.read()
        if mirror:
            frame = cv2.flip(frame, 1)
        image = make_resnet(frame)
        cv2.imshow('frame',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

def main():
    x = 0
    while(x != 4):
        x = int(input("Press 1 for image, 2 for video, 3 for live stream , 4 to exit window \n"))
        if (x == 1):
            image = input("Enter name of image : ")
            resnet_image(image)
        if (x == 2):
            video = input("Enter name of video : ")
            resnet_video(video)
        if (x == 3):
            print("Press q to exit\n")
            resnet_live()
# Press 'q' to quit.
main()
