import unittest
import os

from downloaders import ImageDownloader


class ImageDownloaderTestCase(unittest.TestCase):
    """
    Tests that test my ImageDownloader class.
    Not starting any extra test-specific dummy webservers here, though. Using existing one on local machine for now.
    In production testing, would use (local mirror of) team's CI server env for this.
    """

    def setUp(self):
        self.existing_testfile = "urls_testdata.txt"
        self.nonexist_testfile = "less_testdata.txt"

        self.urls = [
            "fdfhttp://127.0.0.1:8081/textures/wood.jpg",
            #"http://127.0.0.1:8081/textures/kitchen.jpg",
            "http://127.0.0.1:8081/textures/gridjpg",
            "",
            "",
            "vjkdfs"
        ]
        self.expected_status_ok = [
            False,
            #True,
            False,
            False,
            False,
            False
        ]
        self.expected_filenames = [
            "",
            #"51cdebb4642726305401839ea38fbedd029eabaafc53aaac1599fdf8fe668ee0.jpg",
            "",
            "",
            "",
            ""
        ]

        # write urls txt file:
        with open(self.existing_testfile, 'w') as fh:
            fh.write('\n'.join(self.urls))

        # make sure nonexistent txt file really doesn't exist:
        if os.path.isfile(self.nonexist_testfile):
            os.remove(self.nonexist_testfile)

    def tearDown(self):
        # clean up input file:
        os.remove(self.existing_testfile)
        # clean up any downloaded files:
        for filename in self.expected_filenames:
            if os.path.isfile(filename):
                os.remove(filename)

    def test_constructor_existingfile_appendendings(self):
        """ Check if object can be created when file exists and appendendings switch is True """
        imdl = ImageDownloader(urls_filename=self.existing_testfile, append_known_endings=True)
        self.assertIsNotNone(imdl)

    def test_constructor_nonexistingfile_appendendings(self):
        """ Check if object can be created when file does not exist and appendendings switch is True """
        with self.assertRaises(FileNotFoundError):
            imdl = ImageDownloader(urls_filename=self.nonexist_testfile, append_known_endings=True)

    def test_constructor_existingfile_noappendendings(self):
        """ Check if object can be created when file exists and appendendings switch is False"""
        imdl = ImageDownloader(urls_filename=self.existing_testfile, append_known_endings=False)
        self.assertIsNotNone(imdl)

    def test_constructor_nonexistingfile_noappendendings(self):
        """ Check if object can be created when file does not exist and appendendings switch is False """
        with self.assertRaises(FileNotFoundError):
            imdl = ImageDownloader(urls_filename=self.nonexist_testfile, append_known_endings=False)

    def test_compute_unique_filename_on_disk_appendendings(self):
        """ Check if url hashing is repeatable with appended endings """

        url = "http://127.0.0.1:8081/textures/kitchen.jpg"
        filename_on_disk = "51cdebb4642726305401839ea38fbedd029eabaafc53aaac1599fdf8fe668ee0.jpg"
        append_known_endings = True

        imdl = ImageDownloader(urls_filename=self.existing_testfile, append_known_endings=append_known_endings)

        self.assertEqual(filename_on_disk, imdl.compute_unique_filename_on_disk(url))

    def test_compute_unique_filename_on_disk_noappendendings(self):
        """ Check if url hashing is repeatable without appended endings """

        url = "http://127.0.0.1:8081/textures/kitchen.jpg"
        filename_on_disk = "51cdebb4642726305401839ea38fbedd029eabaafc53aaac1599fdf8fe668ee0"
        append_known_endings = False

        imdl = ImageDownloader(urls_filename=self.existing_testfile, append_known_endings=append_known_endings)

        self.assertEqual(filename_on_disk, imdl.compute_unique_filename_on_disk(url))

    def test_compute_unique_filename_on_disk_appendendings_unknownending(self):
        """ Check that the file naming function appends endings only when they are known. """

        url = "http://127.0.0.1:8081/textures/kitchen.jpg');drop table students;"  # xkcd.com/327 ;)
        filename_on_disk = "b0df614b250e56e3ddb7c9f0c7b1c1bc5d070d8c3356d84aefb46657e8e4afe0"
        append_known_endings = True

        imdl = ImageDownloader(urls_filename=self.existing_testfile, append_known_endings=append_known_endings)

        self.assertEqual(filename_on_disk, imdl.compute_unique_filename_on_disk(url))

    def test_download_single_url(self):
        """ Check if downloading single urls works. """

        imdl = ImageDownloader(urls_filename=self.existing_testfile)

        for urlid in range(len(self.urls)):
            url = self.urls[urlid]
            expected_ok = self.expected_status_ok[urlid]

            infodict = imdl.download_single_url(url)
            if expected_ok:
                self.assertEqual("Ok", infodict['status'])
            else:
                self.assertNotEqual("Ok", infodict['status'])

    def test_download_all_with_feedback(self):
        """ Check if the returned status_info list-of-dicts reflects what we would expect """

        imdl = ImageDownloader(urls_filename=self.existing_testfile)
        status_info = imdl.download_all_with_feedback()

        self.assertIsNotNone(status_info)
        self.assertEqual(len(self.expected_status_ok), len(status_info))
        for i, is_ok in enumerate(self.expected_status_ok):
            if is_ok:
                self.assertEqual("Ok", status_info[i]['status'])
            else:
                self.assertNotEqual("Ok", status_info[i]['status'])

    def test_download_all_standalone(self):
        """ Check if files really were created on disk """

        imdl = ImageDownloader(urls_filename=self.existing_testfile)
        imdl.download_all_standalone()

        for i, filename in enumerate(self.expected_filenames):

            if filename:  # if not empty name:
                self.assertTrue(os.path.isfile(filename))
            else:
                self.assertFalse(os.path.isfile(filename))


if __name__ == "__main__":
    unittest.main()
