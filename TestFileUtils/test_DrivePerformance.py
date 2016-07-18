import unittest
import os
from Utilities import DrivePerformance


class DrivePerformanceTestCase(unittest.TestCase):
    def test_DriveData_with_defaults(self):
        drive_data = DrivePerformance.DriveData()

        expected = ',0,0,0,0,0,0,0,0,0,0,0,0,0\n'
        self.assertEqual(expected, str(drive_data))

    def test_DriveData_data_fields(self):
        drive_data = DrivePerformance.DriveData()
        drive_data.description = 'New Drive'
        drive_data.run_number = 4
        drive_data.seq_read = 1.1
        drive_data.seq_write = 2.2
        drive_data.rand_read_512 = 3.3
        drive_data.rand_write_512 = 4.4
        drive_data.rand_read_4k_QD_1 = 5.5
        drive_data.rand_read_4k_QD_1_IOPS = 6.6
        drive_data.rand_write_4k_QD_1 = 7.7
        drive_data.rand_write_4k_QD_1_IOPS = 8.8
        drive_data.rand_read_4k_QD_32 = 9.9
        drive_data.rand_read_4k_QD_32_IOPS = 10.10
        drive_data.rand_write_4k_QD_32 = 11.11
        drive_data.rand_write_4k_QD_32_IOPS = 12.12
        expected = 'New Drive,4,1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,10.1,11.11,12.12\n'
        self.assertEqual(expected, str(drive_data))

    def test_print_header_labels(self):
        expected = 'Drive,Run Number,Sequential Read,Sequential Write,Random Read 512KB,Random Write 512KB,' + \
               'Random Read 4KB (QD=1),' 'Random Read 4KB (QD=1) IOPS,Random Write 4KB (QD=1),' + \
               'Random Write 4KB (QD=1) IOPS,Random Read 4KB (QD=32),Random Read 4KB (QD=32) IOPS,' + \
               'Random Write 4KB (QD=32),Random Write 4KB (QD=32) IOPS\n'

        self.assertEqual(expected, DrivePerformance.DriveData.print_header_labels())

    def test_read_file(self):
        file = os.getcwd() + os.sep + 'resources' + os.sep + 'test_data.txt'
        ret_lines = DrivePerformance.read_file(file, True)
        self.assertEquals(45, len(ret_lines))

    def test_build_drive_list_all_fields(self):
        test_lines = ['480G mSATA Run 1',
                      'Sequential Read :   519.697 MB/s',
                      'Sequential Write :   449.736 MB/s',
                      'Random Read 512KB :   368.688 MB/s',
                      'Random Write 512KB :   436.907 MB/s',
                      'Random Read 4KB (QD=1) :    32.642 MB/s [  7969.3 IOPS]',
                      'Random Write 4KB (QD=1) :   103.845 MB/s [ 25352.9 IOPS]',
                      'Random Read 4KB (QD=32) :   300.546 MB/s [ 73375.4 IOPS]',
                      'line should not be read',
                      'Random Write 4KB (QD=32) :   299.240 MB/s [ 73056.6 IOPS]]']
        ret_drives = DrivePerformance.build_drive_list(test_lines, True)
        self.assertEquals(1, len(ret_drives))
        drive = ret_drives[0]
        self.assertEquals('480G:mSATA', drive.description)
        self.assertEquals('1', drive.run_number)
        self.assertEquals('519.697', drive.seq_read)
        self.assertEquals('449.736', drive.seq_write)
        self.assertEquals('368.688', drive.rand_read_512)
        self.assertEquals('436.907', drive.rand_write_512)
        self.assertEquals('32.642', drive.rand_read_4k_QD_1)
        self.assertEquals('7969.3', drive.rand_read_4k_QD_1_IOPS)
        self.assertEquals('103.845', drive.rand_write_4k_QD_1)
        self.assertEquals('25352.9', drive.rand_write_4k_QD_1_IOPS)
        self.assertEquals('300.546', drive.rand_read_4k_QD_32)
        self.assertEquals('73375.4', drive.rand_read_4k_QD_32_IOPS)
        self.assertEquals('299.240', drive.rand_write_4k_QD_32)
        self.assertEquals('73056.6', drive.rand_write_4k_QD_32_IOPS)

    # def test_build_drive_list_one_field_match(self):
    #     test_lines = ['This is not a match!', '480G:mSATA']
    #     ret_drives = DrivePerformance.build_drive_list(test_lines)
    #     drive = ret_drives[0]
    #     self.assertEquals('480G:mSATA', drive.description)
    #     # check one other field for the default value
    #     self.assertEqual('0', drive.run_number)


if __name__ == '__main__':
    unittest.main()
