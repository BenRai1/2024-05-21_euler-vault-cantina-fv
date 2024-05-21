// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;
import {ERC20} from "../../../lib/ethereum-vault-connector/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Governance.sol";



contract GovernanceHarness is Governance, AbstractBaseHarness {
    using TypesLib for uint16;
    constructor(Integrations memory integrations) Governance (integrations) {}

    function getOnBehalfOfAccountHarness() external returns (address onBehalfOfAccount) {
        return EVCAuthenticateGovernor();
    }

    function getCFG_MAX_VALUEHarness() external returns (uint32) {
        return CFG_MAX_VALUE;
    }

    function getOP_MAX_VALUEHarness() external returns (uint32) {
        return OP_MAX_VALUE;
    }

    function toConfigAmountHarness(uint16 value) external returns (ConfigAmount) {
        return value.toConfigAmount();
    }
}