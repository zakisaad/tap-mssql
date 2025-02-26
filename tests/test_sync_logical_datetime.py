"""
Test tap discovery
"""
from datetime import date, datetime, timezone, time, timedelta
from dateutil.tz import tzoffset

from tap_tester import menagerie, runner

from database import drop_all_user_databases, create_database, \
    create_table, mssql_cursor_context_manager, insert, delete_by_pk, update_by_pk, enable_database_tracking

from base import BaseTapTest


class SyncDateLogical(BaseTapTest):
    """ Test the tap discovery """

    EXPECTED_METADATA = dict()

    def name(self):
        return "{}_logical_sync_datetime_test".format(super().name())

    @classmethod
    def discovery_expected_metadata(cls):
        """The expected streams and metadata about the streams"""

        return cls.EXPECTED_METADATA

    @classmethod
    def setUpClass(cls) -> None:
        """Create the expected schema in the test database"""

        database_name = "data_types_database"
        schema_name = "dbo"
        drop_all_user_databases()

        values = [
            (
                0,
                date(1, 1, 1),
                datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
                datetime(1, 1, 1, 0, 0, tzinfo=timezone.utc),
                datetime(1, 1, 1, 13, 46, tzinfo=timezone(timedelta(hours=-14))).isoformat(),
                datetime(1900, 1, 1, 0, 0, tzinfo=timezone.utc),
                time(0, 0, tzinfo=timezone.utc)),
            (
                1,
                date(9999, 12, 31),
                datetime(9999, 12, 31, 23, 59, 59, 997000, tzinfo=timezone.utc),
                datetime(9999, 12, 31, 23, 59, 59, 999000, tzinfo=timezone.utc),
                datetime(9999, 12, 31, 10, 14, tzinfo=timezone(timedelta(hours=14))).isoformat(),
                datetime(2079, 6, 6, 23, 59, tzinfo=timezone.utc),
                time(23, 59, 59, tzinfo=timezone.utc)),
            (2, None, None, None, None, None, None),
            (
                3,
                date(4533, 6, 9),
                datetime(3099, 2, 6, 4, 27, 37, 983000, tzinfo=timezone.utc),
                datetime(9085, 4, 30, 21, 52, 57, 492920, tzinfo=timezone.utc),
                datetime(5749, 4, 3, 1, 47, 47, 110809, tzinfo=timezone(timedelta(hours=10, minutes=5))).isoformat(),
                datetime(2031, 4, 30, 19, 32, tzinfo=timezone.utc),
                time(21, 9, 56, 0, tzinfo=timezone.utc)),
            (
                4,
                date(3476, 10, 14),
                datetime(7491, 4, 5, 8, 46, 0, 360000, tzinfo=timezone.utc),
                datetime(8366, 7, 13, 17, 15, 10, 102386, tzinfo=timezone.utc),
                datetime(2642, 6, 19, 21, 10, 28, 546280, tzinfo=timezone(timedelta(hours=6, minutes=15))).isoformat(),
                datetime(2024, 6, 22, 0, 36, tzinfo=timezone.utc),
                time(2, 14, 4, 0, tzinfo=timezone.utc))]

        schema = {
            'selected': True,
            'properties': {
                'its_time': {
                    'selected': True,
                    'inclusion': 'available',
                    'type': ['string', 'null']},
                'pk': {
                    'maximum': 2147483647,
                    'selected': True,
                    'inclusion': 'automatic',
                    'type': ['integer'],
                    'minimum': -2147483648},
                'just_a_date': {
                    'selected': True,
                    'inclusion': 'available',
                    'type': ['string', 'null'],
                    'format': 'date-time'},
                'date_and_time': {
                    'selected': True,
                    'inclusion': 'available',
                    'type': ['string', 'null'],
                    'format': 'date-time'},
                "bigger_range_and_precision_datetime": {
                    'selected': True,
                    'inclusion': 'available',
                    'type': ['string', 'null'],
                    'format': 'date-time'},
                "datetime_with_timezones": {
                    'selected': True,
                    'inclusion': 'available',
                    'type': ['string', 'null'],
                    'format': 'date-time'},
                "datetime_no_seconds": {
                    'selected': True,
                    'inclusion': 'available',
                    'type': ['string', 'null'],
                    'format': 'date-time'},
                "_sdc_deleted_at": {'format': 'date-time', 'type': ['string', 'null']}},
            'type': 'object'}

        feilds = [
            {'pk': {'sql-datatype': 'int', 'selected-by-default': True, 'inclusion': 'automatic'}},
            {'just_a_date': {'sql-datatype': 'date', 'selected-by-default': True, 'inclusion': 'available'}},
            {'date_and_time': {'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'available'}},
            {'bigger_range_and_precision_datetime': {'sql-datatype': 'datetime2', 'selected-by-default': True, 'inclusion': 'available'}},
            {'datetime_with_timezones': {'sql-datatype': 'datetimeoffest', 'selected-by-default': True, 'inclusion': 'available'}},
            {'datetime_no_seconds': {'sql-datatype': 'smalldatetime', 'selected-by-default': True, 'inclusion': 'available'}},
            {'its_time': {'sql-datatype': 'time', 'selected-by-default': True, 'inclusion': 'available'}}]

        query_list = list(create_database(database_name, "Latin1_General_CS_AS"))
        query_list.extend(enable_database_tracking(database_name))

        table_name = "dates_and_times"
        primary_key = {"pk"}

        column_name = ["pk", "just_a_date", "date_and_time", "bigger_range_and_precision_datetime",
                       "datetime_with_timezones", "datetime_no_seconds", "its_time"]
        column_type = ["int", "date", "datetime", "datetime2", "datetimeoffset", "smalldatetime", "time"]

        column_def = [" ".join(x) for x in list(zip(column_name, column_type))]
        query_list.extend(create_table(database_name, schema_name, table_name, column_def,
                                       primary_key=primary_key, tracking=True))
        query_list.extend(insert(database_name, schema_name, table_name, values))

        mssql_cursor_context_manager(*query_list)

        values = [
            (
                0,
                date(1, 1, 1),
                datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
                datetime(1, 1, 1, 0, 0, tzinfo=timezone.utc),
                datetime(1, 1, 1, 13, 46, tzinfo=timezone(timedelta(hours=-14))).astimezone(timezone.utc),
                datetime(1900, 1, 1, 0, 0, tzinfo=timezone.utc),
                time(0, 0, tzinfo=timezone.utc)),
            (
                1,
                date(9999, 12, 31),
                datetime(9999, 12, 31, 23, 59, 59, 997000, tzinfo=timezone.utc),
                datetime(9999, 12, 31, 23, 59, 59, 999000, tzinfo=timezone.utc),
                datetime(9999, 12, 31, 10, 14, tzinfo=timezone(timedelta(hours=14))).astimezone(timezone.utc),
                datetime(2079, 6, 6, 23, 59, tzinfo=timezone.utc),
                time(23, 59, 59, tzinfo=timezone.utc)),
            (2, None, None, None, None, None, None),
            (
                3,
                date(4533, 6, 9),
                datetime(3099, 2, 6, 4, 27, 37, 983000, tzinfo=timezone.utc),
                datetime(9085, 4, 30, 21, 52, 57, 492920, tzinfo=timezone.utc),
                datetime(5749, 4, 3, 1, 47, 47, 110809,
                         tzinfo=timezone(timedelta(hours=10, minutes=5))).astimezone(timezone.utc),
                datetime(2031, 4, 30, 19, 32, tzinfo=timezone.utc),
                time(21, 9, 56, 0, tzinfo=timezone.utc)),
            (
                4,
                date(3476, 10, 14),
                datetime(7491, 4, 5, 8, 46, 0, 360000, tzinfo=timezone.utc),
                datetime(8366, 7, 13, 17, 15, 10, 102386, tzinfo=timezone.utc),
                datetime(2642, 6, 19, 21, 10, 28, 546280,
                         tzinfo=timezone(timedelta(hours=6, minutes=15))).astimezone(timezone.utc),
                datetime(2024, 6, 22, 0, 36, tzinfo=timezone.utc),
                time(2, 14, 4, 0, tzinfo=timezone.utc))]
        cls.EXPECTED_METADATA = {
            '{}_{}_{}'.format(database_name, schema_name, table_name): {
                'is-view': False,
                'schema-name': schema_name,
                'row-count': 0,
                'values': values,
                'table-key-properties': primary_key,
                'selected': None,
                'database-name': database_name,
                'stream_name': table_name,
                'fields': feilds,
                'schema': schema}
        }
        cls.expected_metadata = cls.discovery_expected_metadata

    def test_run(self):
        """
        Verify that a full sync can send capture all data and send it in the correct format
        for integer and boolean (bit) data.
        Verify that the fist sync sends an activate immediately.
        Verify that the table version is incremented up
        """

        print("running test {}".format(self.name()))

        conn_id = self.create_connection()

        # run in check mode
        check_job_name = runner.run_check_mode(self, conn_id)

        # verify check  exit codes
        exit_status = menagerie.get_exit_status(conn_id, check_job_name)
        menagerie.verify_check_exit_status(self, exit_status, check_job_name)

        # get the catalog information of discovery
        found_catalogs = menagerie.get_catalogs(conn_id)
        additional_md = [{"breadcrumb": [], "metadata": {'replication-method': 'LOG_BASED'}}]
        BaseTapTest.select_all_streams_and_fields(
            conn_id, found_catalogs, additional_md=additional_md)

        # run a sync and verify exit codes
        record_count_by_stream = self.run_sync(conn_id, clear_state=True)

        # verify record counts of streams
        expected_count = {k: len(v['values']) for k, v in self.expected_metadata().items()}
        # self.assertEqual(record_count_by_stream, expected_count)

        # verify records match on the first sync
        records_by_stream = runner.get_records_from_target_output()

        table_version = dict()
        for stream in self.expected_streams():
            with self.subTest(stream=stream):
                stream_expected_data = self.expected_metadata()[stream]
                table_version[stream] = records_by_stream[stream]['table_version']

                # verify on the first sync you get
                # activate version message before and after all data for the full table
                # and before the logical replication part
                if records_by_stream[stream]['messages'][-1].get("data"):
                    last_row_data = True
                else:
                    last_row_data = False

                self.assertEqual(
                    records_by_stream[stream]['messages'][0]['action'],
                    'activate_version')
                self.assertEqual(
                    records_by_stream[stream]['messages'][-2]['action'],
                    'activate_version')
                if last_row_data:
                    self.assertEqual(
                        records_by_stream[stream]['messages'][-3]['action'],
                        'activate_version')
                else:
                    self.assertEqual(
                        records_by_stream[stream]['messages'][-1]['action'],
                        'activate_version')
                self.assertEqual(
                    len([m for m in records_by_stream[stream]['messages'][1:] if m["action"] == "activate_version"]),
                    2,
                    msg="Expect 2 more activate version messages for end of full table and beginning of log based")

                column_names = [
                    list(field_data.keys())[0] for field_data in stream_expected_data[self.FIELDS]
                ]

                expected_messages = [
                    {
                        "action": "upsert", "data":
                        {
                            column: value for column, value
                            in list(zip(column_names, stream_expected_data[self.VALUES][row]))
                        }
                    } for row in range(len(stream_expected_data[self.VALUES]))
                ]

                # Verify all data is correct for the full table part
                if last_row_data:
                    final_row = -3
                else:
                    final_row = -2

                for expected_row, actual_row in list(
                        zip(expected_messages, records_by_stream[stream]['messages'][1:final_row])):
                    with self.subTest(expected_row=expected_row):

                        self.assertEqual(actual_row["action"], "upsert")
                        self.assertEqual(len(expected_row["data"].keys()), len(actual_row["data"].keys()),
                                         msg="there are not the same number of columns")
                        for column_name, expected_value in expected_row["data"].items():
                            if isinstance(expected_value, datetime):
                                # sql server only keeps milliseconds not microseconds
                                self.assertEqual(
                                    expected_value.isoformat().replace('000+00:00', 'Z').replace('+00:00', 'Z'),
                                    actual_row["data"][column_name],
                                    msg="expected: {} != actual {}".format(
                                        expected_value.isoformat().replace('000+00:00', 'Z').replace('+00:00', 'Z'),
                                        actual_row["data"][column_name]))
                            elif isinstance(expected_value, time):
                                # sql server time has second resolution only
                                self.assertEqual(
                                    expected_value.replace(microsecond=0).isoformat().replace('+00:00', ''),
                                    actual_row["data"][column_name],
                                    msg="expected: {} != actual {}".format(
                                        expected_value.isoformat().replace('+00:00', 'Z'),
                                        actual_row["data"][column_name]))
                            elif isinstance(expected_value, date):
                                # sql server time has second resolution only
                                self.assertEqual(expected_value.isoformat() + 'T00:00:00+00:00',
                                                 actual_row["data"][column_name],
                                                 msg="expected: {} != actual {}".format(
                                                     expected_value.isoformat()+ 'T00:00:00+00:00',
                                                     actual_row["data"][column_name]))
                            else:
                                self.assertEqual(expected_value, actual_row["data"][column_name],
                                                 msg="expected: {} != actual {}".format(
                                                     expected_value, actual_row["data"][column_name]))

                # Verify all data is correct for the log replication part if sent
                if records_by_stream[stream]['messages'][-1].get("data"):
                    for column_name, expected_value in expected_messages[-1]["data"].items():
                        if isinstance(expected_value, datetime):
                            # sql server only keeps milliseconds not microseconds
                            self.assertEqual(
                                expected_value.isoformat().replace('000+00:00', 'Z').replace('+00:00', 'Z'),
                                actual_row["data"][column_name],
                                msg="expected: {} != actual {}".format(
                                    expected_value.isoformat().replace('000+00:00', 'Z').replace('+00:00', 'Z'),
                                    actual_row["data"][column_name]))
                        elif isinstance(expected_value, time):
                            # sql server time has second resolution only
                            self.assertEqual(expected_value.replace(microsecond=0).isoformat().replace('+00:00', ''),
                                             actual_row["data"][column_name],
                                             msg="expected: {} != actual {}".format(
                                                 expected_value.isoformat().replace('+00:00', 'Z'),
                                                 actual_row["data"][column_name]))
                        elif isinstance(expected_value, date):
                            # sql server time has second resolution only
                            self.assertEqual(expected_value.isoformat() + 'T00:00:00+00:00',
                                             actual_row["data"][column_name],
                                             msg="expected: {} != actual {}".format(
                                                 expected_value.isoformat() + 'T00:00:00+00:00',
                                                 actual_row["data"][column_name]))
                        else:
                            self.assertEqual(expected_value, actual_row["data"][column_name],
                                             msg="expected: {} != actual {}".format(
                                                 expected_value, actual_row["data"][column_name]))

                print("records are correct for stream {}".format(stream))

                # verify state and bookmarks
                state = menagerie.get_state(conn_id)
                bookmark = state['bookmarks'][stream]

                self.assertIsNone(state.get('currently_syncing'), msg="expected state's currently_syncing to be None")
                self.assertIsNotNone(
                    bookmark.get('current_log_version'),
                    msg="expected bookmark to have current_log_version because we are using log replication")
                self.assertTrue(bookmark['initial_full_table_complete'], msg="expected full table to be complete")
                inital_log_version = bookmark['current_log_version']

                self.assertEqual(bookmark['version'], table_version[stream],
                                 msg="expected bookmark for stream to match version")

                expected_schemas = self.expected_metadata()[stream]['schema']
                self.assertEqual(records_by_stream[stream]['schema'],
                                 expected_schemas,
                                 msg="expected: {} != actual: {}".format(expected_schemas,
                                                                         records_by_stream[stream]['schema']))

        # ----------------------------------------------------------------------
        # invoke the sync job AGAIN and after insert, update, delete or rows
        # ----------------------------------------------------------------------

        database_name = "data_types_database"
        schema_name = "dbo"
        table_name = "dates_and_times"
        column_name = ["pk", "just_a_date", "date_and_time", "bigger_range_and_precision_datetime",
                       "datetime_with_timezones", "datetime_no_seconds", "its_time"]
        new_date_value = datetime(2019, 7, 22, 21, 11, 40, 573000)
        insert_value = [(
            6,
            new_date_value.date(),
            new_date_value,
            datetime(9085, 4, 30, 21, 52, 57, 492920, tzinfo=timezone.utc),
            datetime(5749, 4, 3, 1, 47, 47, 110809, tzinfo=timezone(timedelta(hours=10, minutes=5))).isoformat(),
            datetime(2031, 4, 30, 19, 32, tzinfo=timezone.utc),
            time(21, 9, 56, 0, tzinfo=timezone.utc))]
        update_value = [(
            2,
            new_date_value.date(),
            new_date_value,
            datetime(9085, 4, 30, 21, 52, 57, 492920, tzinfo=timezone.utc),
            datetime(5749, 4, 3, 1, 47, 47, 110809, tzinfo=timezone(timedelta(hours=10, minutes=5))).isoformat(),
            datetime(2031, 4, 30, 19, 32, tzinfo=timezone.utc),
            time(21, 9, 56, 0, tzinfo=timezone.utc))]
        delete_value = [(3, )]
        query_list = (insert(database_name, schema_name, table_name, insert_value))
        query_list.extend(delete_by_pk(database_name, schema_name, table_name, delete_value, column_name[:1]))
        query_list.extend(update_by_pk(database_name, schema_name, table_name, update_value, column_name))
        mssql_cursor_context_manager(*query_list)
        insert_value = [(
            6,
            new_date_value.date(),
            new_date_value,
            datetime(9085, 4, 30, 21, 52, 57, 492920, tzinfo=timezone.utc),
            datetime(5749, 4, 3, 1, 47, 47, 110809, tzinfo=timezone(timedelta(hours=10, minutes=5))).astimezone(timezone.utc),
            datetime(2031, 4, 30, 19, 32, tzinfo=timezone.utc),
            time(21, 9, 56, 0, tzinfo=timezone.utc))]
        update_value = [(
            2,
            new_date_value.date(),
            new_date_value,
            datetime(9085, 4, 30, 21, 52, 57, 492920, tzinfo=timezone.utc),
            datetime(5749, 4, 3, 1, 47, 47, 110809, tzinfo=timezone(timedelta(hours=10, minutes=5))).astimezone(timezone.utc),
            datetime(2031, 4, 30, 19, 32, tzinfo=timezone.utc),
            time(21, 9, 56, 0, tzinfo=timezone.utc))]
        insert_value = [insert_value[0] + (None, )]
        update_value = [update_value[0] + (None, )]
        delete_value = [(3, None, None, None, None, None, None, datetime.utcnow())]
        self.EXPECTED_METADATA["data_types_database_dbo_dates_and_times"]["values"] =  \
            [self.expected_metadata()["data_types_database_dbo_dates_and_times"]["values"][-1]] + \
            insert_value + delete_value + update_value
        self.EXPECTED_METADATA["data_types_database_dbo_dates_and_times"]["fields"].append(
            {"_sdc_deleted_at": {
                'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'automatic'}})

        # run a sync and verify exit codes
        record_count_by_stream = self.run_sync(conn_id)

        expected_count = {k: len(v['values']) for k, v in self.expected_metadata().items()}
        self.assertEqual(record_count_by_stream, expected_count)
        records_by_stream = runner.get_records_from_target_output()

        for stream in self.expected_streams():
            with self.subTest(stream=stream):
                stream_expected_data = self.expected_metadata()[stream]
                new_table_version = records_by_stream[stream]['table_version']

                # verify on a subsequent sync you get activate version message only after all data
                self.assertEqual(
                    records_by_stream[stream]['messages'][0]['action'],
                    'activate_version')
                self.assertTrue(all(
                    [message["action"] == "upsert" for message in records_by_stream[stream]['messages'][1:]]
                ))

                column_names = [
                    list(field_data.keys())[0] for field_data in stream_expected_data[self.FIELDS]
                ]

                expected_messages = [
                    {
                        "action": "upsert", "data":
                        {
                            column: value for column, value
                            in list(zip(column_names, stream_expected_data[self.VALUES][row]))
                        }
                    } for row in range(len(stream_expected_data[self.VALUES]))
                ]

                # remove sequences from actual values for comparison
                [message.pop("sequence") for message
                 in records_by_stream[stream]['messages'][1:]]

                # Verify all data is correct
                for expected_row, actual_row in list(
                        zip(expected_messages, records_by_stream[stream]['messages'][1:])):
                    with self.subTest(expected_row=expected_row):
                        self.assertEqual(actual_row["action"], "upsert")

                        # we only send the _sdc_deleted_at column for deleted rows
                        self.assertGreaterEqual(len(expected_row["data"].keys()), len(actual_row["data"].keys()),
                                         msg="there are not the same number of columns")

                        for column_name, expected_value in expected_row["data"].items():
                            if column_name != "_sdc_deleted_at":
                                if isinstance(expected_value, datetime):
                                    # sql server only keeps milliseconds not microseconds
                                    self.assertEqual(
                                        expected_value.isoformat().replace('000+00:00', 'Z').replace('+00:00', 'Z').replace('000', 'Z'),
                                        actual_row["data"][column_name],
                                        msg="expected: {} != actual {}".format(
                                            expected_value.isoformat().replace('000+00:00', 'Z').replace('+00:00', 'Z').replace('000', 'Z'),
                                            actual_row["data"][column_name]))
                                elif isinstance(expected_value, time):
                                    # sql server time has second resolution only
                                    self.assertEqual(
                                        expected_value.replace(microsecond=0).isoformat().replace('+00:00', ''),
                                        actual_row["data"][column_name],
                                        msg="expected: {} != actual {}".format(
                                            expected_value.isoformat().replace('+00:00', 'Z'),
                                            actual_row["data"][column_name]))
                                elif isinstance(expected_value, date):
                                    # sql server time has second resolution only
                                    self.assertEqual(expected_value.isoformat() + 'T00:00:00+00:00',
                                                     actual_row["data"][column_name],
                                                     msg="expected: {} != actual {}".format(
                                                         expected_value.isoformat() + 'T00:00:00+00:00',
                                                         actual_row["data"][column_name]))
                                else:
                                    self.assertEqual(expected_value, actual_row["data"][column_name],
                                                     msg="expected: {} != actual {}".format(
                                                         expected_value, actual_row["data"][column_name]))

                            elif expected_value:
                                # we have an expected value for a deleted row
                                try:
                                    actual_value = datetime.strptime(actual_row["data"][column_name],
                                                                     "%Y-%m-%dT%H:%M:%S.%fZ")
                                except ValueError:
                                    actual_value = datetime.strptime(actual_row["data"][column_name],
                                                                     "%Y-%m-%dT%H:%M:%SZ")
                                self.assertGreaterEqual(actual_value, expected_value - timedelta(seconds=15))
                                self.assertLessEqual(actual_value, expected_value + timedelta(seconds=15))
                            else:
                                # the row wasn't deleted so we can either not pass the column or it can be None
                                self.assertIsNone(actual_row["data"].get(column_name))

                print("records are correct for stream {}".format(stream))

                # verify state and bookmarks
                state = menagerie.get_state(conn_id)
                bookmark = state['bookmarks'][stream]

                self.assertIsNone(state.get('currently_syncing'), msg="expected state's currently_syncing to be None")
                self.assertIsNotNone(
                    bookmark.get('current_log_version'),
                    msg="expected bookmark to have current_log_version because we are using log replication")
                self.assertTrue(bookmark['initial_full_table_complete'], msg="expected full table to be complete")
                new_log_version = bookmark['current_log_version']
                self.assertGreater(new_log_version, inital_log_version,
                                   msg='expected log version to increase')

                self.assertEqual(bookmark['version'], table_version[stream],
                                 msg="expected bookmark for stream to match version")
                self.assertEqual(bookmark['version'], new_table_version,
                                 msg="expected bookmark for stream to match version")

                expected_schemas = self.expected_metadata()[stream]['schema']
                self.assertEqual(records_by_stream[stream]['schema'],
                                 expected_schemas,
                                 msg="expected: {} != actual: {}".format(expected_schemas,
                                                                         records_by_stream[stream]['schema']))
