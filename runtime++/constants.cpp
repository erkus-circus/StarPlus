
// for transforming a short into an int
int shortToInt(unsigned char byte1, unsigned char byte2)
{
    // no idea if this works copilot gave it to me
    return (int)byte1 << 8 | byte2;
}

/// TODO: this no work.
int fourBytesToInt(unsigned char *buf)
{
    return (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3];
}