# zschema sub-schema for zgrab2's mysql module (modules/mysql.go)
# Registers zgrab2-mysql globally, and mysql with the main zgrab2 schema.
from zschema.leaves import *
from zschema.compounds import *
import zschema.registry

import zcrypto_schemas.zcrypto as zcrypto
import zgrab2

from zgrab2 import DebugOnly

# zgrab2/lib/mysql/mysql.go: GetServerStatusFlags()
mysql_server_status_flags = zgrab2.FlagsSet([
    "SERVER_STATUS_IN_TRANS",
    "SERVER_STATUS_AUTOCOMMIT",
    "SERVER_MORE_RESULTS_EXISTS",
    "SERVER_QUERY_NO_GOOD_INDEX_USED",
    "SERVER_QUERY_NO_INDEX_USED",
    "SERVER_STATUS_CURSOR_EXISTS",
    "SERVER_STATUS_LAST_ROW_SENT",
    "SERVER_STATUS_DB_DROPPED",
    "SERVER_STATUS_NO_BACKSLASH_ESCAPES",
    "SERVER_STATUS_METADATA_CHANGED",
    "SERVER_QUERY_WAS_SLOW",
    "SERVER_PS_OUT_PARAMS",
    "SERVER_STATUS_IN_TRANS_READONLY",
    "SERVER_SESSION_STATE_CHANGED",
], required=True, doc="The set of status flags the server returned in the initial HandshakePacket. Each entry corresponds to a bit being set in the flags; key names correspond to the #defines in the MySQL docs.")

# zgrab2/lib/mysql/mysql.go: GetClientCapabilityFlags()
mysql_capability_flags = zgrab2.FlagsSet([
    "CLIENT_LONG_PASSWORD",
    "CLIENT_FOUND_ROWS",
    "CLIENT_LONG_FLAG",
    "CLIENT_CONNECT_WITH_DB",
    "CLIENT_NO_SCHEMA",
    "CLIENT_COMPRESS",
    "CLIENT_ODBC",
    "CLIENT_LOCAL_FILES",
    "CLIENT_IGNORE_SPACE",
    "CLIENT_PROTOCOL_41",
    "CLIENT_INTERACTIVE",
    "CLIENT_SSL",
    "CLIENT_IGNORE_SIGPIPE",
    "CLIENT_TRANSACTIONS",
    "CLIENT_RESERVED",
    "CLIENT_SECURE_CONNECTION",
    "CLIENT_MULTI_STATEMENTS",
    "CLIENT_MULTI_RESULTS",
    "CLIENT_PS_MULTI_RESULTS",
    "CLIENT_PLUGIN_AUTH",
    "CLIENT_CONNECT_ATTRS",
    "CLIENT_PLUGIN_AUTH_LEN_ENC_CLIENT_DATA",
    "CLIENT_CAN_HANDLE_EXPIRED_PASSWORDS",
    "CLIENT_SESSION_TRACK",
    "CLIENT_DEPRECATED_EOF",
], doc="The set of capability flags the server returned in the initial HandshakePacket. Each entry corresponds to a bit being set in the flags; key names correspond to the #defines in the MySQL docs.")

# zgrab2/modules/mysql.go: MySQLScanResults
mysql_scan_response = SubRecord({
    "result": SubRecord({
        "protocol_version": Unsigned8BitInteger(required=True, doc="8-bit unsigned integer representing the server's protocol version sent in the initial HandshakePacket from the server.", examples=["10"]),
        "server_version": String(required=True, doc="The specific server version returned in the initial HandshakePacket. Often in the form x.y.z, but not always.", examples=["5.5.58", "5.6.38", "5.7.20", "8.0.3-rc-log"]),
        "connection_id": DebugOnly(Unsigned32BitInteger(doc="The server's internal identifier for this client's connection, sent in the initial HandshakePacket.")),
        "auth_plugin_data": DebugOnly(Binary(doc="Optional plugin-specific data, whose meaning depends on the value of auth_plugin_name. Returned in the initial HandshakePacket.")),
        "capability_flags": mysql_capability_flags,
        "character_set": DebugOnly(Unsigned8BitInteger(doc="The identifier for the character set the server is using. Returned in the initial HandshakePacket.")),
        "status_flags": mysql_server_status_flags,
        "auth_plugin_name": DebugOnly(String(doc="The name of the authentication plugin, returned in the initial HandshakePacket.")),
        "error_code": Signed32BitInteger(doc="Only set if there is an error returned by the server, for example if the scanner is not on the allowed hosts list."),
        "error_message": String(doc="Optional string describing the error. Only set if there is an error."),
        "raw_packets": ListOf(Binary(), doc="The base64 encoding of all packets sent and received during the scan."),
        "tls": zgrab2.tls_log,
    })
}, extends=zgrab2.base_scan_response)

zschema.registry.register_schema("zgrab2-mysql", mysql_scan_response)

zgrab2.register_scan_response_type('mysql', mysql_scan_response)
