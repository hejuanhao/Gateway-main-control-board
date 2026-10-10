class LEDScreenProtocol:
    def __init__(self):
        pass

    def _calculate_crc16(self, data: bytes) -> bytes:
        """核心校验算法：计算CRC-16/XMODEM (小端序返回)"""
        crc = 0x0000
        for b in data:
            crc ^= (b << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = ((crc << 1) ^ 0x1021) & 0xFFFF
                else:
                    crc = (crc << 1) & 0xFFFF
        # 返回低字节在前、高字节在后
        return bytes([crc & 0xFF, (crc >> 8) & 0xFF])

    def _build_frame(self, address: int, payload: bytes) -> bytes:
        """将数据打包成完整帧"""
        # 地址位处理：255 -> 00 FF
        addr_bytes = bytes([address >> 8, address & 0xFF])

        # 总长度 = 帧头(1) + 地址(2) + 长度(1) + 载荷(n) + CRC(2) + 帧尾(1)
        total_length = 1 + 2 + 1 + len(payload) + 2 + 1

        # 参与CRC校验的数据：地址 + 长度 + 载荷
        data_to_crc = addr_bytes + bytes([total_length]) + payload
        crc_bytes = self._calculate_crc16(data_to_crc)

        # 完整帧： 53 + 校验数据 + 校验码 + 40
        frame = bytes([0x53]) + data_to_crc + crc_bytes + bytes([0x40])
        return frame

    def clear_screen(self, address: int = 255) -> bytes:
        """生成【清屏】指令"""
        payload = bytes([0x10])  # 10 为清屏指令码
        return self._build_frame(address, payload)

    def set_text(self, address: int, x: int, y: int, font_size: int, color: int, text: str) -> bytes:
        """生成【显示文本】指令"""
        # 文字转为 GB2312 编码
        text_bytes = text.encode('gb2312')

        # 按照协议顺序拼接载荷 (Payload)
        payload = bytearray()
        payload.append(0x17)  # 命令字: 17 (显示文本)
        payload.extend(x.to_bytes(2, 'little'))  # X坐标: 2字节小端
        payload.extend(y.to_bytes(2, 'little'))  # Y坐标: 2字节小端
        payload.append(0x01)  # 固定参数
        payload.append(len(text_bytes))  # 文本字节长度
        payload.append(0x01)  # 固定参数
        payload.append(font_size)  # 字体大小 (如 12(0x0C), 16(0x10))
        payload.append(color)  # 颜色/属性 (如 1)
        payload.extend(text_bytes)  # 具体的文字内容

        return self._build_frame(address, bytes(payload))


if __name__ == '__main__':
    screen = LEDScreenProtocol()
    frame_data = screen.set_text(255, 0, 25, 16, 1, '地面监测端一有火')

    # 关键：转成 空格分隔的大写十六进制格式
    hex_str = ' '.join(f'{byte:02X}' for byte in frame_data)
    print(hex_str)