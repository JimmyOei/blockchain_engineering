from asyncio import run

from ipv8.community import Community, CommunitySettings
from ipv8.configuration import ConfigBuilder, Strategy, WalkerDefinition, default_bootstrap_defs
from ipv8.util import run_forever
from ipv8_service import IPv8
from ipv8.peer import Peer
from ipv8.peerdiscovery.network import PeerObserver
from ipv8.messaging.payload import Payload
from ipv8.lazy_community import lazy_wrapper
from miner import mine

COMMUNITY_ID = bytes.fromhex("2c1cc6e35ff484f99ebdfb6108477783c0102881")
SERVER_PUBLIC_KEY = bytes.fromhex("4c69624e61434c504b3a86b23934a28d669c390e2d1fc0b0870706c4591cc0cb178bc5a811da6d87d27ef319b2638ef60cc8d119724f4c53a1ebfad919c3ac4136c501ce5c09364e0ebb")
TU_DELFT_EMAIL = "J.T.Oei-1@student.tudelft.nl"
GITHUB_URL = "https://github.com/JimmyOei/blockchain_engineering"
NONCE = mine(TU_DELFT_EMAIL, GITHUB_URL)

# Submission Message (message_id = 1)
# | Field        | Logical Type | IPv8 Wire Format | Description |
# |--------------|--------------|------------------|-------------|
# | `email`      | UTF-8 string | `varlenHutf8`    | Your TU Delft email address |
# | `github_url` | UTF-8 string | `varlenHutf8`    | URL of your public GitHub repo |
# | `nonce`      | integer      | `q`              | The nonce that solves the PoW |
class SubmissionPayload(Payload):
    msg_id = 1
    format_list = ["varlenHutf8", "varlenHutf8", "q"]
  
    def __init__(self, email: str, github_url: str, nonce: int):
        self.email = email
        self.github_url = github_url
        self.nonce = nonce
    
    def to_pack_list(self) -> list:
        return [("varlenHutf8", self.email), ("varlenHutf8", self.github_url), ("q", self.nonce)]
      
    @classmethod
    def from_unpack_list(cls: type["SubmissionPayload"], email: str, github_url: str, nonce: int) -> "SubmissionPayload":
        return cls(email, github_url, nonce)

# Server Response (message_id = 2)
# | Field     | Logical Type | IPv8 Wire Format | Description |
# |-----------|--------------|------------------|-------------|
# | `success` | boolean      | `?`              | `True` if your submission is accepted |
# | `message` | UTF-8 string | `varlenHutf8`    | Human-readable result |
class ResponsePayload(Payload):
    msg_id = 2
    format_list = ["?", "varlenHutf8"]
  
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message
    
    def to_pack_list(self) -> list:
        return [("?", self.success), ("varlenHutf8", self.message)]
      
    @classmethod
    def from_unpack_list(cls: type["ResponsePayload"], success: bool, message: str) -> "ResponsePayload":
        return cls(success, message)


class Lab1Community(Community, PeerObserver):
    community_id = COMMUNITY_ID
    
    def __init__(self, settings: CommunitySettings) -> None:
        super().__init__(settings)
        
        self.add_message_handler(ResponsePayload, self.on_message)
        
        self.submission_sent = False
        print("Initialized Lab1Community")
    
    def on_peer_added(self, peer: Peer) -> None:
        print("I am:", self.my_peer, "I found:", peer)
        
        if not self.submission_sent and peer.public_key.key_to_bin() == SERVER_PUBLIC_KEY:
            print("Found the server", peer)
            print("Sending submission to the server...")
            self.ez_send(peer, SubmissionPayload(TU_DELFT_EMAIL, GITHUB_URL, NONCE))
            self.submission_sent = True
            print("Submission sent")

    def on_peer_removed(self, peer: Peer) -> None:
        pass

    def started(self) -> None:
        self.network.add_peer_observer(self)
        
    @lazy_wrapper(ResponsePayload)
    def on_message(self, peer: Peer, payload: ResponsePayload) -> None:
        print("Received a message from", peer, ":", payload.success, payload.message)


async def start_communities() -> None:
    builder = ConfigBuilder().clear_keys().clear_overlays()

    builder.add_key("labs peer", "curve25519", f"labs-ec.pem")

    builder.add_overlay("Lab1Community", "labs peer",
                        [WalkerDefinition(Strategy.RandomWalk,
                                          10, {"timeout": 3.0})],
                        default_bootstrap_defs, {}, [("started",)])
    await IPv8(builder.finalize(),
                   extra_communities={"Lab1Community": Lab1Community}).start()
    await run_forever()

run(start_communities())