"""
Test tap discovery
"""
from datetime import datetime, timedelta

from tap_tester import menagerie, runner

from database import drop_all_user_databases, create_database, \
    create_table, mssql_cursor_context_manager, insert, enable_database_tracking, update_by_pk, delete_by_pk, \
    create_schema

from base import BaseTapTest


class SyncMultLogical(BaseTapTest):
    """ Test the tap discovery """

    EXPECTED_METADATA = dict()

    def name(self):
        return "{}_logical_sync_multiple_test".format(super().name())

    @classmethod
    def discovery_expected_metadata(cls):
        """The expected streams and metadata about the streams"""

        return cls.EXPECTED_METADATA

    @classmethod
    def setUpClass(cls) -> None:
        """Create the expected schema in the test database"""

        drop_all_user_databases()
        database_name = "database_name"
        query_list = list(create_database(database_name, "Latin1_General_CS_AS"))
        query_list.extend(enable_database_tracking(database_name))

        schema_name = "schema_name"
        query_list.extend(create_schema(database_name, schema_name))

        table_name = "table_name"
        fields = [
            {'pk': {'sql-datatype': 'int', 'selected-by-default': True, 'inclusion': 'automatic'}},
            {'column_name': {'sql-datatype': 'int', 'selected-by-default': True, 'inclusion': 'available'}}]
        schema = {
            'type': 'object',
            'properties': {
                'column_name': {
                    'type': ['integer', 'null'],
                    'minimum': -2147483648,
                    'maximum': 2147483647,
                    'inclusion': 'available',
                    'selected': True},
                'pk':
                    {'type': ['integer'],
                     'minimum': -2147483648,
                     'maximum': 2147483647,
                     'inclusion': 'automatic',
                     'selected': True},
                "_sdc_deleted_at": {'format': 'date-time', 'type': ['string', 'null']}},
            'selected': True}

        cls.EXPECTED_METADATA = {
            '{}_{}_{}'.format(database_name, schema_name, table_name): {
                'is-view': False,
                'schema-name': schema_name,
                'row-count': 0,
                'values': [
                    (0, 1),
                    (1, 2)],
                'table-key-properties': {'pk'},
                'selected': None,
                'database-name': database_name,
                'stream_name': table_name,
                'fields': fields,
                'schema': schema},
        }

        column_name = ["pk", "column_name"]
        column_type = ["int", "int"]
        primary_key = {"pk"}
        column_def = [" ".join(x) for x in list(zip(column_name, column_type))]
        query_list.extend(create_table(database_name, schema_name, table_name, column_def,
                                       primary_key=primary_key, tracking=True))
        query_list.extend(insert(database_name, schema_name, table_name,
                                 cls.EXPECTED_METADATA['{}_{}_{}'.format(
                                     database_name, schema_name, table_name)]["values"]))

        table_name = "TABLE_NAME"

        cls.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)] = {
            'is-view': False,
            'schema-name': schema_name,
            'row-count': 0,
            'values': [
                (0, 3),
                (1, 4)],
            'table-key-properties': {'pk'},
            'selected': None,
            'database-name': database_name,
            'stream_name': table_name,
            'fields': fields,
            'schema': schema
        }

        column_name = ["pk", "column_name"]
        column_type = ["int", "int"]
        primary_key = {"pk"}
        column_def = [" ".join(x) for x in list(zip(column_name, column_type))]
        query_list.extend(create_table(database_name, schema_name, table_name, column_def,
                                       primary_key=primary_key, tracking=True))
        query_list.extend(insert(database_name, schema_name, table_name,
                                 cls.EXPECTED_METADATA['{}_{}_{}'.format(
                                     database_name, schema_name, table_name)]["values"]))

        schema_name = "SCHEMA_NAME"
        query_list.extend(create_schema(database_name, schema_name))

        table_name = "table_name"

        cls.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)] = {
            'is-view': False,
            'schema-name': schema_name,
            'row-count': 0,
            'values': [
                (0, 5),
                (1, 6)],
            'table-key-properties': {'pk'},
            'selected': None,
            'database-name': database_name,
            'stream_name': table_name,
            'fields': fields,
            'schema': schema
        }

        column_name = ["pk", "column_name"]
        column_type = ["int", "int"]
        primary_key = {"pk"}
        column_def = [" ".join(x) for x in list(zip(column_name, column_type))]
        query_list.extend(create_table(database_name, schema_name, table_name, column_def,
                                       primary_key=primary_key, tracking=True))
        query_list.extend(insert(database_name, schema_name, table_name,
                                 cls.EXPECTED_METADATA['{}_{}_{}'.format(
                                     database_name, schema_name, table_name)]["values"]))

        table_name = "TABLE_NAME"

        cls.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)] = {
            'is-view': False,
            'schema-name': schema_name,
            'row-count': 0,
            'values': [
                (0, 7),
                (1, 8)],
            'table-key-properties': {'pk'},
            'selected': None,
            'database-name': database_name,
            'stream_name': table_name,
            'fields': fields,
            'schema': schema
        }

        column_name = ["pk", "column_name"]
        column_type = ["int", "int"]
        primary_key = {"pk"}
        column_def = [" ".join(x) for x in list(zip(column_name, column_type))]
        query_list.extend(create_table(database_name, schema_name, table_name, column_def,
                                       primary_key=primary_key, tracking=True))
        query_list.extend(insert(database_name, schema_name, table_name,
                                 cls.EXPECTED_METADATA['{}_{}_{}'.format(
                                     database_name, schema_name, table_name)]["values"]))

        database_name = "DATABASE_NAME_NO_COLLISION"
        query_list.extend(create_database(database_name, "Latin1_General_CS_AS"))
        query_list.extend(enable_database_tracking(database_name))

        schema_name = "schema_name"
        query_list.extend(create_schema(database_name, schema_name))

        table_name = "table_name"

        cls.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)] = {
            'is-view': False,
            'schema-name': schema_name,
            'row-count': 0,
            'values': [
                (0, 9),
                (1, 10)],
            'table-key-properties': {'pk'},
            'selected': None,
            'database-name': database_name,
            'stream_name': table_name,
            'fields': fields,
            'schema': schema
        }

        column_name = ["pk", "column_name"]
        column_type = ["int", "int"]
        primary_key = {"pk"}
        column_def = [" ".join(x) for x in list(zip(column_name, column_type))]
        query_list.extend(create_table(database_name, schema_name, table_name, column_def,
                                       primary_key=primary_key, tracking=True))
        query_list.extend(insert(database_name, schema_name, table_name,
                                 cls.EXPECTED_METADATA['{}_{}_{}'.format(
                                     database_name, schema_name, table_name)]["values"]))

        table_name = "TABLE_NAME"

        cls.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)] = {
            'is-view': False,
            'schema-name': schema_name,
            'row-count': 0,
            'values': [
                (0, 11),
                (1, 12)],
            'table-key-properties': {'pk'},
            'selected': None,
            'database-name': database_name,
            'stream_name': table_name,
            'fields': fields,
            'schema': schema
        }

        column_name = ["pk", "column_name"]
        column_type = ["int", "int"]
        primary_key = {"pk"}
        column_def = [" ".join(x) for x in list(zip(column_name, column_type))]
        query_list.extend(create_table(database_name, schema_name, table_name, column_def,
                                       primary_key=primary_key, tracking=True))
        query_list.extend(insert(database_name, schema_name, table_name,
                                 cls.EXPECTED_METADATA['{}_{}_{}'.format(
                                     database_name, schema_name, table_name)]["values"]))

        schema_name = "SCHEMA_NAME"
        query_list.extend(create_schema(database_name, schema_name))

        table_name = "table_name"

        cls.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)] = {
            'is-view': False,
            'schema-name': schema_name,
            'row-count': 0,
            'values': [
                (0, 13),
                (1, 14)],
            'table-key-properties': {'pk'},
            'selected': None,
            'database-name': database_name,
            'stream_name': table_name,
            'fields': fields,
            'schema': schema
        }

        column_name = ["pk", "column_name"]
        column_type = ["int", "int"]
        primary_key = {"pk"}
        column_def = [" ".join(x) for x in list(zip(column_name, column_type))]
        query_list.extend(create_table(database_name, schema_name, table_name, column_def,
                                       primary_key=primary_key, tracking=True))
        query_list.extend(insert(database_name, schema_name, table_name,
                                 cls.EXPECTED_METADATA['{}_{}_{}'.format(
                                     database_name, schema_name, table_name)]["values"]))

        table_name = "TABLE_NAME"

        cls.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)] = {
            'is-view': False,
            'schema-name': schema_name,
            'row-count': 0,
            'values': [
                (0, 15),
                (1, 16)],
            'table-key-properties': {'pk'},
            'selected': None,
            'database-name': database_name,
            'stream_name': table_name,
            'fields': fields,
            'schema': schema
        }

        column_name = ["pk", "column_name"]
        column_type = ["int", "int"]
        primary_key = {"pk"}
        column_def = [" ".join(x) for x in list(zip(column_name, column_type))]
        query_list.extend(create_table(database_name, schema_name, table_name, column_def,
                                       primary_key=primary_key, tracking=True))
        query_list.extend(insert(database_name, schema_name, table_name,
                                 cls.EXPECTED_METADATA['{}_{}_{}'.format(
                                     database_name, schema_name, table_name)]["values"]))

        mssql_cursor_context_manager(*query_list)
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
                            self.assertEqual(expected_value, actual_row["data"][column_name],
                                             msg="expected: {} != actual {}".format(
                                                 expected_row, actual_row))

                # Verify all data is correct for the log replication part if sent
                if records_by_stream[stream]['messages'][-1].get("data"):
                    for column_name, expected_value in expected_messages[-1]["data"].items():
                        self.assertEqual(expected_value,
                                         records_by_stream[stream]['messages'][-1]["data"][column_name],
                                         msg="expected: {} != actual {}".format(
                                             expected_row, actual_row))

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

        database_name = "database_name"
        schema_name = "schema_name"
        table_name = "table_name"
        column_name = ["pk", "column_name"]
        insert_value = [(2, 100)]
        update_value = [(0, 101,)]
        delete_value = [(1, )]
        query_list = (insert(database_name, schema_name, table_name, insert_value))
        query_list.extend(delete_by_pk(database_name, schema_name, table_name, delete_value, column_name[:1]))
        query_list.extend(update_by_pk(database_name, schema_name, table_name, update_value, column_name))
        mssql_cursor_context_manager(*query_list)
        meta_insert_value = [insert_value[0] + (None,)]
        meta_update_value = [update_value[0] + (None,)]
        meta_delete_value = [delete_value[0] + (None, datetime.utcnow())]
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["values"] = \
            meta_insert_value + meta_delete_value + meta_update_value
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["fields"].append(
            {"_sdc_deleted_at": {
                'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'automatic'}}
        )

        table_name = "TABLE_NAME"
        column_name = ["pk", "column_name"]
        query_list = (insert(database_name, schema_name, table_name, insert_value))
        query_list.extend(delete_by_pk(database_name, schema_name, table_name, delete_value, column_name[:1]))
        query_list.extend(update_by_pk(database_name, schema_name, table_name, update_value, column_name))
        mssql_cursor_context_manager(*query_list)
        meta_delete_value = [delete_value[0] + (None, datetime.utcnow())]
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["values"] = \
            meta_insert_value + meta_delete_value + meta_update_value
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["fields"].append(
            {"_sdc_deleted_at": {
                'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'automatic'}}
        )

        schema_name = "SCHEMA_NAME"
        table_name = "table_name"
        column_name = ["pk", "column_name"]
        query_list = (insert(database_name, schema_name, table_name, insert_value))
        query_list.extend(delete_by_pk(database_name, schema_name, table_name, delete_value, column_name[:1]))
        query_list.extend(update_by_pk(database_name, schema_name, table_name, update_value, column_name))
        mssql_cursor_context_manager(*query_list)
        meta_delete_value = [delete_value[0] + (None, datetime.utcnow())]
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["values"] = \
            meta_insert_value + meta_delete_value + meta_update_value
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["fields"].append(
            {"_sdc_deleted_at": {
                'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'automatic'}}
        )

        table_name = "TABLE_NAME"
        column_name = ["pk", "column_name"]
        query_list = (insert(database_name, schema_name, table_name, insert_value))
        query_list.extend(delete_by_pk(database_name, schema_name, table_name, delete_value, column_name[:1]))
        query_list.extend(update_by_pk(database_name, schema_name, table_name, update_value, column_name))
        mssql_cursor_context_manager(*query_list)
        meta_delete_value = [delete_value[0] + (None, datetime.utcnow())]
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["values"] = \
            meta_insert_value + meta_delete_value + meta_update_value
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["fields"].append(
            {"_sdc_deleted_at": {
                'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'automatic'}}
        )

        database_name = "DATABASE_NAME_NO_COLLISION"
        schema_name = "schema_name"
        table_name = "table_name"
        column_name = ["pk", "column_name"]
        query_list = (insert(database_name, schema_name, table_name, insert_value))
        query_list.extend(delete_by_pk(database_name, schema_name, table_name, delete_value, column_name[:1]))
        query_list.extend(update_by_pk(database_name, schema_name, table_name, update_value, column_name))
        mssql_cursor_context_manager(*query_list)
        meta_delete_value = [delete_value[0] + (None, datetime.utcnow())]
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["values"] = \
            meta_insert_value + meta_delete_value + meta_update_value
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["fields"].append(
            {"_sdc_deleted_at": {
                'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'automatic'}}
        )

        table_name = "TABLE_NAME"
        column_name = ["pk", "column_name"]
        query_list = (insert(database_name, schema_name, table_name, insert_value))
        query_list.extend(delete_by_pk(database_name, schema_name, table_name, delete_value, column_name[:1]))
        query_list.extend(update_by_pk(database_name, schema_name, table_name, update_value, column_name))
        mssql_cursor_context_manager(*query_list)
        meta_delete_value = [delete_value[0] + (None, datetime.utcnow())]
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["values"] = \
            meta_insert_value + meta_delete_value + meta_update_value
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["fields"].append(
            {"_sdc_deleted_at": {
                'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'automatic'}}
        )

        schema_name = "SCHEMA_NAME"
        table_name = "table_name"
        column_name = ["pk", "column_name"]
        query_list = (insert(database_name, schema_name, table_name, insert_value))
        query_list.extend(delete_by_pk(database_name, schema_name, table_name, delete_value, column_name[:1]))
        query_list.extend(update_by_pk(database_name, schema_name, table_name, update_value, column_name))
        mssql_cursor_context_manager(*query_list)
        meta_delete_value = [delete_value[0] + (None, datetime.utcnow())]
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["values"] = \
            meta_insert_value + meta_delete_value + meta_update_value
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["fields"].append(
            {"_sdc_deleted_at": {
                'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'automatic'}}
        )

        table_name = "TABLE_NAME"
        column_name = ["pk", "column_name"]
        query_list = (insert(database_name, schema_name, table_name, insert_value))
        query_list.extend(delete_by_pk(database_name, schema_name, table_name, delete_value, column_name[:1]))
        query_list.extend(update_by_pk(database_name, schema_name, table_name, update_value, column_name))
        mssql_cursor_context_manager(*query_list)
        meta_delete_value = [delete_value[0] + (None, datetime.utcnow())]
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["values"] = \
            meta_insert_value + meta_delete_value + meta_update_value
        self.EXPECTED_METADATA['{}_{}_{}'.format(database_name, schema_name, table_name)]["fields"].append(
            {"_sdc_deleted_at": {
                'sql-datatype': 'datetime', 'selected-by-default': True, 'inclusion': 'automatic'}}
        )

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
                                self.assertEqual(expected_value, actual_row["data"][column_name],
                                                 msg="expected: {} != actual {}".format(
                                                     expected_row, actual_row))
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
