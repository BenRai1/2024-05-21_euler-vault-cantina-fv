// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;
import "../../src/EVault/shared/types/Types.sol";

contract Type{

struct LiquidationCache {
    address liquidator;
    address violator;
    address collateral;
    address[] collaterals;
    Assets liability;
    Assets repay;
    uint256 yieldBalance;
}

struct UserStorage {
    // Shares and debt balances, balance forwarder opt-in
    PackedUserSlot data;
    // Snapshot of the interest accumulator from the last change to account's liability
    uint256 interestAccumulator;
    // A mapping with allowances for the vault shares token (eToken)
    mapping(address spender => uint256 allowance) eTokenAllowance;
}

}