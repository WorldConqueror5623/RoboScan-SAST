// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Vulnerable {
    mapping(address => uint) public balances;
    address public owner;

    // 🚨 BUG 1 (CRITICAL): Missing Access Control
    // Your tool looks for "public" + ".transfer" + no "onlyOwner"
    function emergencyDrain() public {
        payable(msg.sender).transfer(address(this).balance); 
    }

    // 🚨 BUG 2 (HIGH): Reentrancy
    // Your tool looks for ".call{value:"
    function withdraw() public {
        uint bal = balances[msg.sender];
        require(bal > 0);
        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent, "Failed to send");
        balances[msg.sender] = 0;
    }

    // 🚨 BUG 3 (MEDIUM): Phishing
    // Your tool looks for "tx.origin"
    function setOwner(address newOwner) public {
        require(tx.origin == msg.sender, "Not Owner");
        owner = newOwner;
    }
}