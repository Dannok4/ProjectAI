import os
from Seeker import *
import unittest
from Board import *
# def check_announce_in_listening_radius(seeker_position, hider_announce, listening_radius):
#     x_seeker, y_seeker = seeker_position
#     x_announce, y_announce = hider_announce

#     # Tính khoảng cách Manhattan giữa seeker và tín hiệu thông báo từ hider
#     distance = abs(x_seeker - x_announce) + abs(y_seeker - y_announce)

#     # Nếu khoảng cách nhỏ hơn hoặc bằng bán kính lắng nghe, trả về True và vị trí của thông báo
#     if distance <= listening_radius:
#         return True, hider_announce
#     else:
#         return False, None

# # Sử dụng hàm
# seeker_position = (3, 5)  # Vị trí của seeker
# hider_announce = (7, 8)    # Vị trí thông báo từ hider
# listening_radius = 3       # Bán kính lắng nghe của seeker

# is_announce_in_listening_radius, announce_position = check_announce_in_listening_radius(seeker_position, hider_announce, listening_radius)

# if is_announce_in_listening_radius:
#     print("Thông báo từ hider nằm trong bán kính lắng nghe của seeker.")
#     print("Vị trí của thông báo:", announce_position)
# else:
#     print("Thông báo từ hider không nằm trong bán kính lắng nghe của seeker.")
import unittest

class TestSeekerMethods(unittest.TestCase):
    def test_setVision(self):
        # Tạo một thể hiện của lớp Seeker
        seeker = Seeker(5, 5)  # Giả sử vị trí ban đầu của seeker là (5, 5)

        # Thiết lập các giá trị cần thiết cho seeker và game_map
        seeker.vision_radius = 3
        seeker.bound = (10, 10)  # Giả sử kích thước của bản đồ là 10x10
        seeker.game_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # Gọi phương thức setVision
        vision = seeker.setVision()

        # Kiểm tra kích thước của tầm nhìn
        expected_vision_size = (2 * seeker.vision_radius + 1) ** 2
        self.assertEqual(len(vision), expected_vision_size, "Kích thước của tầm nhìn không chính xác")
        for row in vision:
            self.assertEqual(len(row), 2 * seeker.vision_radius + 1, "Kích thước của tầm nhìn không chính xác")

if __name__ == '__main__':
    unittest.main()
