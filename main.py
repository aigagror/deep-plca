import argparse

import data
import models
import train
import plots

parser = argparse.ArgumentParser()

# Data
parser.add_argument('--data', type=str, help='dataset')
parser.add_argument('--imsize', type=int, help='square image siz')
parser.add_argument('--prob', action='store_true',
                    help='makes the images probability distributions')

# Model
parser.add_argument('--model', choices=['pcla', 'ae', 'al'],
                    help='deep pcla, auto encoder, auto layer')
parser.add_argument('--zdim', type=int, default=None,
                    help='dimension of the embedding space. only for encoders')
parser.add_argument('--new', action='store_true',
                    help='use new weights instead of loading weights from previous run')
parser.add_argument('--nkern', type=int, default=None,
                    help='number of kernels. only for pcla')
parser.add_argument('--kern-size', type=int, default=None,
                    help='kernel size. only for pcla')

# Training
parser.add_argument('--opt', type=str, help='optimizer')
parser.add_argument('--bsz', type=int, help='batch size')
parser.add_argument('--lr', type=float, help='learning rate')
parser.add_argument('--epochs', type=int)

# Losses
parser.add_argument('--recon', choices=['ce', 'bce', 'mse', 'kl'],
                    help='reconstruction loss. [cross entropy, binary cross entropy, mean squared error]')
parser.add_argument('--beta1', type=float, help='impulse entropy weight')
parser.add_argument('--beta2', type=float,
                    help='feature (kernel) entropy weight')
parser.add_argument('--beta3', type=float,
                    help='prior entropy weight')


def main(args):
    # Load data
    train_loader, test_loader, channels = data.load_data(args, shuffle=True,
                                                         droplast=True)

    # Make the model
    model = models.make_model(args, channels)

    # Load weights?
    models.optionally_load_wts(args, model)

    # Train
    metrics = train.train(args, model, train_loader, test_loader)

    # Plot work
    plots.plot_metrics(metrics)
    imgs, _ = next(iter(train_loader))
    plots.plot_recon(args, imgs[:1], model)
