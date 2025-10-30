# Euler V2 Formal Verification Contest Repo

This repo was submitted by me (BenRai1) for the [Euler V2 Audit + Certora Formal Verification competition](https://cantina.xyz/competitions/41306bb9-2bb8-4da6-95c3-66b85e11639f/leaderboard) on Cantina running from the 20th of May 2024 to 17th of June 2024.

The goal of the formal verification part of the competition was to formally verify the following contracts using the Certora Prover:

| Contract                                                                                                                       | SLOC |
| ------------------------------------------------------------------------------------------------------------------------------ | ---- |
| [Borrowing.sol](https://github.com/BenRai1/2024-05-21_euler-vault-cantina-fv/blob/master/src/EVault/modules/Borrowing.sol)     | 102  |
| [Governance.sol](https://github.com/BenRai1/2024-05-21_euler-vault-cantina-fv/blob/master/src/EVault/modules/Governance.sol)   | 216  |
| [Liquidation.sol](https://github.com/BenRai1/2024-05-21_euler-vault-cantina-fv/blob/master/src/EVault/modules/Liquidation.sol) | 116  |
| [RiskManager.sol](https://github.com/BenRai1/2024-05-21_euler-vault-cantina-fv/blob/master/src/EVault/modules/RiskManager.sol) | 55   |
| [Vault.sol](https://github.com/BenRai1/2024-05-21_euler-vault-cantina-fv/blob/master/src/EVault/modules/Vault.sol)             | 158  |

The [rules I wrote](https://github.com/BenRai1/silo-v2-cantina-fv/tree/main/certora/specs) caught 21 out of 27 mutations used for [evaluating the submissions](https://docs.google.com/spreadsheets/d/134AlmLXV2gbSRmsgCdK0IRU2qQtL6XhJL4uiOLayn5A/edit?gid=1970712821#gid=1970712821) which place me 2nd in the FV contest.
