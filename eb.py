import spidev
spi = spidev.SpiDev()
spi.open(0,CHIP_SELECT_0_OR_1)
spi.max_speed_hz = 1000000
spi.xfer([value_8bit})

