// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

//import the abstarct contract
import "../../../src/EVault/shared/LTVUtils.sol";
import "../AbstractBaseHarness.sol";

contract LTVUtilsHarness is LTVUtils, AbstractBaseHarness {

    constructor(Integrations memory integrations) Base(integrations) {}

    function getLTVHarness(address collateral, bool liquidation) public view returns (ConfigAmount) {
        return getLTV(collateral, liquidation);
    }

    function isRecognizedCollateralHarness(address collateral) public view returns (bool) {
        return isRecognizedCollateral(collateral);
    }

    function getLTVConfigHarness(address collateral) public view returns (LTVConfig memory) {
        return vaultStorage.ltvLookup[collateral];
    }

    function getCollateralLTV(address collateral) public view returns (LTVConfig memory) {
        return vaultStorage.ltvLookup[collateral];
    }

    function getCurrentLiquidationLTV(LTVConfig memory config) public view returns (ConfigAmount) {
        uint256 currentLiquidationLTV = config.initialLiquidationLTV.toUint16();

        unchecked {
            uint256 targetLiquidationLTV = config.liquidationLTV.toUint16();
            uint256 timeRemaining = config.targetTimestamp - block.timestamp;

            // targetLiquidationLTV < initialLiquidationLTV and timeRemaining <= rampDuration
            currentLiquidationLTV = targetLiquidationLTV
                + (currentLiquidationLTV - targetLiquidationLTV) * timeRemaining / config.rampDuration;
        }

        // because ramping happens only when liquidation LTV decreases, it's safe to down-cast the new value
        return ConfigAmount.wrap(uint16(currentLiquidationLTV));
    }
}