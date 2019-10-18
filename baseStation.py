import spidev

spi = spidev.SpiDev()
spi.open(0,0)

resp = spi.xfer2([0x00])
print(resp[0])

spi.close()

