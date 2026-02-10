import numpy as np
from aicsimageio import AICSImage

from RESPAN.ImageAnalysis.tifffile_compat import imwrite

SUPPORTED_EXTENSIONS = (
    ".tif",
    ".tiff",
    ".czi",
    ".nd2",
    ".lif",
    ".vsi",
    ".ims",
    ".oib",
    ".oif",
    ".ndpi",
    ".vms",
    ".svs",
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
)


def is_image_file(filename):
    """
    Check if a file is a supported image format.
    """
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)


def imread(path, logger=None):
    """
    Read an image from disk using AICSImageIO.
    Supports many formats (.czi, .nd2, .lif, .tif, etc.)
    Returns a numpy array in ZCYX format if possible.
    """
    if logger:
        logger.info(f"  Reading image with AICSImageIO: {path}")

    img = AICSImage(path)

    # RESPAN generally expects ZCYX or CZYX and uses check_image_shape to normalize.
    # We'll provide ZCYX as a sensible default for AICSImageIO to match common expectations.
    # S=0, T=0 for first scene/timepoint.
    data = img.get_image_data("ZCYX", S=0, T=0)

    return data


def create_and_save_multichannel_tiff(images_3d, filename, bitdepth, settings):
    """
    Create TIF from a list of 3D images, merge them into a image,
    save as a 16-bit TIFF file.

    Args:
        images_3d (list of numpy.ndarray): List of 3D numpy arrays representing input images.
        filename (str): Filename for the output TIFF file.

    Returns:
        none
    """

    # Convert the list of images to a single multichannel image
    multichannel_image = np.stack(images_3d, axis=1)

    # Convert the multichannel image to 16-bit
    multichannel_image = multichannel_image.astype(np.uint16)

    imwrite(
        filename,
        multichannel_image,
        compression="zlib",
        compressionargs=1,
        imagej=True,
        photometric="minisblack",
        metadata={"spacing": settings.input_resZ, "unit": "um", "axes": "ZCYX"},
    )


def create_mip_and_save_multichannel_tiff(images_3d, filename, bitdepth, settings):
    """
    Create MIPs from a list of 3D images, merge them into a multi-channel 2D image,
    save as a 16-bit TIFF file, and return the merged 2D multi-channel image.

    Args:
        images_3d (list of numpy.ndarray): List of 3D numpy arrays representing input images.
        filename (str): Filename for the output TIFF file.

    Returns:
        numpy.ndarray: Merged 2D multi-channel image as a numpy array.
    """
    # Create MIPs from the 3D images
    mips = [np.amax(img, axis=0) for img in images_3d]

    # Convert the MIPs to a single multichannel image
    multichannel_image = np.stack(mips, axis=0)

    # Convert the multichannel image to 16-bit
    multichannel_image = multichannel_image.astype(np.uint16)
    # multichannel_image = rescale_all_channels_to_full_range(multichannel_image)

    # Save the multichannel image as a 16-bit TIFF file
    # imwrite(filename, multichannel_image, photometric='minisblack')

    imwrite(
        filename,
        multichannel_image,
        compression="zlib",
        compressionargs=1,
        imagej=True,
        photometric="minisblack",
        metadata={"spacing": settings.input_resZ, "unit": "um", "axes": "CYX"},
    )

    # Return the merged 2D multi-channel image as a numpy array
    return multichannel_image


def create_mip_and_save_multichannel_tiff_4d(images_3d, filename, bitdepth, settings):
    """
    Create MIPs from a list of 3D images, merge them into a multi-channel 2D image,
    save as a 16-bit TIFF file, and return the merged 2D multi-channel image.

    Args:
        images_3d (list of numpy.ndarray): List of 3D numpy arrays representing input images.
        filename (str): Filename for the output TIFF file.

    Returns:
        numpy.ndarray: Merged 2D multi-channel image as a numpy array.
    """
    # Create MIPs from the 3D images
    mips = [np.amax(img, axis=1) for img in images_3d]

    # Convert the MIPs to a single multichannel image
    multichannel_image = np.stack(mips, axis=0)
    multichannel_image = np.swapaxes(multichannel_image, 0, 1)

    # Convert the multichannel image to 16-bit
    multichannel_image = multichannel_image.astype(np.uint16)
    # multichannel_image = rescale_all_channels_to_full_range(multichannel_image)

    # Save the multichannel image as a 16-bit TIFF file
    # imwrite(filename, multichannel_image, photometric='minisblack')

    imwrite(
        filename,
        multichannel_image,
        compression="zlib",
        compressionargs=1,
        imagej=True,
        photometric="minisblack",
        metadata={"spacing": settings.input_resZ, "unit": "um", "axes": "TCYX"},
    )

    # Return the merged 2D multi-channel image as a numpy array
    return multichannel_image


def rescale_all_channels_to_full_range(array):
    """
    Rescale all channels in a multi-channel numpy array to use the full range of 16-bit values.

    Args:
        array (numpy.ndarray): Input multi-channel numpy array.

    Returns:
        numpy.ndarray: Rescaled multi-channel numpy array.
    """
    num_channels = array.shape[0]

    for channel in range(num_channels):
        # Calculate the minimum and maximum values of the current channel
        min_val = np.min(array[channel])
        max_val = np.max(array[channel])

        # Rescale the current channel to the 16-bit range [0, 65535] using a linear transformation
        array[channel] = (array[channel] - min_val) / (max_val - min_val) * 65535

        # Convert the rescaled channel to uint16 data type
        array[channel] = array[channel].astype(np.uint16)

    return array
