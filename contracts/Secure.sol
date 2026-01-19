// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Secure {
    mapping(address => uint) public balances;
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function withdraw() public {
        uint bal = balances[msg.sender];
        require(bal > 0);
        
        // ✅ FIX: Update state BEFORE sending (Checks-Effects-Interactions)
        balances[msg.sender] = 0;

        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent, "Failed to send Ether");
    }

    function setOwner(address newOwner) public onlyOwner {
        owner = newOwner;
    }
}
