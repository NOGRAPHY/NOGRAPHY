# Import required libaries and functions
import matplotlib.pyplot as plt
import numpy as np
from keras import optimizers, callbacks
from keras.layers import Dense, Convolution2D, MaxPooling2D, Dropout, BatchNormalization, Flatten
from keras.models import Sequential, load_model
from keras.utils import to_categorical
from keras_preprocessing.image import img_to_array
from matplotlib import cm
from sklearn.model_selection import train_test_split
plt.style.use('default')

## Network structure of the CNN for Glyph Recognition
## Definition of a CNN with three hidden convolution and two hidden fully connected layers
class CnnModel:
    def __init__(self, x_train, y_train, x_test, y_test, x_val, y_val, output_layer_size):
        self.X_train = x_train
        self.Y_train = y_train
        self.X_test = x_test
        self.Y_test = y_test
        self.X_val = x_val
        self.Y_val = y_val
        self.output_layer_size = output_layer_size


    def build_model(self):
        # create model
        model = Sequential()

        ## Convolution Layers
        # Convolution Layer 1 (8×8×32) (input = 200×200, black-and-white)
        model.add(Convolution2D(32, kernel_size=(8, 8), activation='relu', input_shape=(200, 200, 1), name="Conv2D_1"))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # Convolution Layer 2 (5×5×64)
        model.add(Convolution2D(64, kernel_size=(5, 5), activation='relu', name="Conv2D_2"))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # Convolution Layer 3 (3×3×32)
        model.add(Convolution2D(32, kernel_size=(3, 3), activation='relu', name="Conv2D_3"))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))

        ## Fully Connected Layers
        model.add(Flatten()) # We flatten() the input to make it easier to work with, since we no longer need its shape.
        # Fully Connected Layer 1 (128 neurons, Activation: relu, Dropout: 0.5)
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))

        # Fully Connected Layer 2 (8 neurons (size from number of perturbed glyphs, Activation: softmax, Dropout: 0.5)
        model.add(Dense(self.output_layer_size, activation='softmax'))
        # output: output is an N-dimensional vector indicating the probability input ist one of perturbed glyphs

        return model

    def compile_model(self, build_model):
        ## Compile model
        # using accuracy to measure model performance and categorical_crossentropy (>2 classes)
        # Define optimizer and network compile parameters
        learning_rate = 10 ** -3
        beta_1 = 0.9
        beta_2 = 0.999
        epsilon = 1e-7
        optimizer_name = 'Adam'
        loss_function = 'categorical_crossentropy'
        metrics = ['accuracy']

        # define adam optimizer
        adam = optimizers.Adam(learning_rate=learning_rate,
                               beta_1=beta_1,
                               beta_2=beta_2,
                               epsilon=epsilon,
                               amsgrad=False,
                               name=optimizer_name)

        # compile model and initialize weights
        build_model.compile(optimizer=adam,
                            loss=loss_function,
                            metrics=metrics,
                            loss_weights=None,
                            weighted_metrics=None,
                            run_eagerly=None)

        return build_model


    def train_model(self, cnn_model):
        ## Network Training
        # Define network training parameters
        batch_size = 15
        epochs = 10 ** 5
        monitor = 'val_loss'
        verbose = 2
        mode = 'min'
        top_model_filepath = "top_model.h5"
        min_delta = 0 # Minimum change in the monitored quantity to qualify as an improvement
        patience = 10 # Number of epochs with no improvement after which training will be stopped

        ## Callback for stop training
        # Stop training when monitored metric 'loss' has stopped improving after 3 epochs.
        # This callback will stop the training when there is no improvement in
        # the validation loss for three consecutive epochs.
        # And save's the best trained model.
        early_stopping = callbacks.EarlyStopping(monitor=monitor, min_delta=min_delta, patience=patience, verbose=verbose, mode=mode)
        checkpoint = callbacks.ModelCheckpoint(top_model_filepath, monitor=monitor, verbose=verbose, save_best_only=True, mode=mode)
        callbacks_list = [early_stopping, checkpoint]

        ## train the model
        # with defined network parameters
        cnn_model.fit(self.X_train, self.Y_train,
                      batch_size=batch_size,
                      epochs=epochs,
                      shuffle=True,
                      verbose=verbose,
                      validation_data=(self.X_test, self.Y_test),
                      callbacks=callbacks_list)

        return cnn_model


    def show_training_development(self, glyph_recognition_model):
        # plot the development of the accuracy during training in first plot
        plt.figure(figsize=(12, 4))

        plt.subplot(1, 2, (1))
        plt.plot(glyph_recognition_model.history['accuracy'], linestyle='-.')
        plt.plot(glyph_recognition_model.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'valid'], loc='lower right')
        plt.grid(True)
        # plt.gca().set_ylim(0, 1) # set the vertical range to [0-1]

        # plot the development of loss during training in second plot
        plt.subplot(1, 2, (2))
        plt.plot(glyph_recognition_model.history['loss'], linestyle='-.')
        plt.plot(glyph_recognition_model.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'valid'], loc='upper right')
        plt.grid(True)
        # plt.gca().set_ylim(0, 1) # set the vertical range to [0-1]


    def show_evaluation(self, glyph_recognition_model):
        verbose = 2 # define output mode

        # evaluate trained model against top model
        # show new trained model loss and accuracy
        score = glyph_recognition_model.evaluate(self.X_val, self.Y_val, verbose=verbose)
        print('Current model ')
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

        # load top trained model and show loss and accuracy
        top_model = load_model('top_model.h5')
        score = top_model.evaluate(self.X_val, self.Y_val, verbose=verbose)
        print('Top model ')
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])


    def predict_glyph(self, glyph_recognition_model, image):
        # convert image into array of numbers
        data = []
        org_img = img_to_array(image)
        data.append(org_img)
        data = np.asarray(data, dtype="float") / 255.0

        # predict nearest class of image with trained model
        class_of_glyph = glyph_recognition_model.predict_classes(data)

        # plot image with predicted class
        class_of_glyph = self.rev_conv_label(int(class_of_glyph[0]))
        fig, ax = plt.subplots(1)
        ax.imshow(image, interpolation='nearest', cmap=cm.gray)
        ax.text(5, 5, class_of_glyph, bbox={'facecolor': 'white', 'pad': 10})
        plt.show()

    @staticmethod
    def conv_label(label):
        if label == 'times':
            return 0
        elif label == 'EmilysCandy-Regular':
            return 1
        elif label == 'PlayfairDisplay-Regular':
            return 2
        elif label == 'Unna-Regular':
            return 3
        elif label == 'Vidaloka-Regular':
            return 4

    @staticmethod
    def rev_conv_label(label):
        if label == 0:
            return 'times'
        elif label == 1:
            return 'EmilysCandy-Regular'
        elif label == 2:
            return 'PlayfairDisplay-Regular'
        elif label == 3:
            return 'Unna-Regular'
        elif label == 4:
            return 'Vidaloka-Regular'

if __name__ == "__main__":


    dataset = np.load('font_dataset.npz')
    # extract the first array with images
    PIL_img_data = dataset['arr_0']
    # extract the second array with class labels
    class_name = dataset['arr_1']
    dataset.close()

    labels = []
    for label in class_name:
        labels.append(CnnModel.conv_label(label))

    # create random train (70%), test (15%) and validation (15%) datasets from loaded images
    x_train, x_test, y_train, y_test = train_test_split(PIL_img_data, labels, test_size=0.3, random_state=42)
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, random_state=42)

    # convert the labels to vectors
    y_train = to_categorical(y_train, num_classes=5)
    y_test = to_categorical(y_test, num_classes=5)
    y_val = to_categorical(y_val, num_classes=5)

    # create class object with train, test, val data and output neuron value
    cnn_Model = CnnModel(x_train, y_train, x_test, y_test, x_val, y_val, 5)

    # build cnn model
    build_model = cnn_Model.build_model()

    # show CNN-Model architecture
    #plot_model(build_model, show_shapes=True, rankdir="LR")
    build_model.summary()

    # compile model with 'Adam' optimizer
    compiled_model = cnn_Model.compile_model(build_model)

    # train model with stop when monitored metric 'loss' has stopped improving after 3 epochs.
    # save model to file, if it is the best
    trained_model = cnn_Model.train_model(compiled_model)

    # show training progress for accuracy and loss
    cnn_Model.show_training_development(trained_model)

    # evaluate model against loaded top model
    cnn_Model.show_evaluation(trained_model)
