# References:
    # https://github.com/KimRass/Conditional-WGAN-GP/blob/main/model.py

import torch
from torch import nn


class ConvBlock(nn.Module):
    def __init__(
        self, channels, out_channels, kernel_size, stride, padding, transposed=False,
    ):
        super().__init__()

        if transposed:
            self.conv = nn.ConvTranspose2d(
                channels,
                out_channels,
                kernel_size,
                stride,
                padding,
                bias=False,
            )
        else:
            self.conv = nn.Conv2d(
                channels,
                out_channels,
                kernel_size,
                stride,
                padding,
                bias=False,
            )
        self.norm = nn.BatchNorm2d(out_channels)
        self.leaky_relu = nn.LeakyReLU(0.2)

    def forward(self, x):
        x = self.conv(x)
        x = self.norm(x)
        x = self.leaky_relu(x)
        return x


class Generator(nn.Module):
    def __init__(self, n_classes, latent_dim, hidden_dim):
        super().__init__()

        self.n_classes = n_classes
        self.latent_dim = latent_dim

        self.conv_block1 = ConvBlock(
            latent_dim + n_classes, hidden_dim * 4, 4, 1, 0, transposed=True,
        )
        self.conv_block2 = ConvBlock(hidden_dim * 4, hidden_dim * 2, 3, 2, 1, transposed=True)
        self.conv_block3 = ConvBlock(hidden_dim * 2, hidden_dim, 4, 2, 1, transposed=True)
        self.conv = nn.ConvTranspose2d(hidden_dim, 1, 4, 2, 1)

    @staticmethod
    def one_hot_encode_label(label, n_classes):
        return torch.eye(n_classes, device=label.device)[label]

    def forward(self, latent_vec, label):
        ohe_label = self.one_hot_encode_label(label=label, n_classes=self.n_classes)
        print(ohe_label)
        x = torch.cat([latent_vec, ohe_label], dim=1)
        x = self.conv_block1(x[..., None, None])
        x = self.conv_block2(x)
        x = self.conv_block3(x)
        x = self.conv(x)
        x = torch.tanh(x)
        return x
