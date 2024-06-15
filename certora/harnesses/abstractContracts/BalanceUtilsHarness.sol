// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

//import the abstarct contract
import "../../../src/EVault/shared/BalanceUtils.sol";
import "../AbstractBaseHarness.sol";

contract BalanceUtilsHarness is BalanceUtils, AbstractBaseHarness {

    constructor(Integrations memory integrations) Base(integrations) {}

    //increaseBalance
    function increaseBalanceHarness(VaultCache memory vaultCache,
        address account,
        address sender,
        Shares amount,
        Assets assets) public {
        increaseBalance(vaultCache, account, sender, amount, assets);
    }
    // decreaseBalance
    function decreaseBalanceHarness(
        VaultCache memory vaultCache,
        address account,
        address sender,
        address receiver,
        Shares amount,
        Assets assets) public {
        decreaseBalance(vaultCache, account, sender, receiver, amount, assets);
    }
    // transferBalance
    function transferBalanceHarness(address from, address to, Shares amount) public {
        transferBalance(from, to, amount);
    }
    // setAllowance
    function setAllowanceHarness(address owner, address spender, uint256 amount) public {
        setAllowance(owner, spender, amount);
    }
    // decreaseAllowance
    function decreaseAllowanceHarness(address owner, address spender, Shares amount) public {
        decreaseAllowance(owner, spender, amount);
    }
    
    function getTotalSharesHarness() external view returns (Shares) {
        return vaultStorage.totalShares;
    }

    function getAllowanceHarness(address owner, address spender) external view returns (uint256) {
        return vaultStorage.users[owner].eTokenAllowance[spender];
    }
}