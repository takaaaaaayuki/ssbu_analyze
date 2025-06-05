class SmashAnalyzer {
    constructor() {
        // 基本設定
        this.config = {
            stage: {
                width: 200,
                height: 100,
                center: { x: 0, y: 0 },
                blastZones: {
                    top: 180,
                    bottom: -140,
                    left: -220,
                    right: 220
                }
            },
            thresholds: {
                damage: {
                    low: 35,
                    medium: 75,
                    high: 100,
                    critical: 150
                },
                guard: {
                    danger: 30,
                    warning: 50,
                    safe: 70
                }
            }
        };

        // キャラクターデータベースの初期化
        this.characterData = new Map([
            ['mario', {
                weight: 98,
                fallSpeed: 1.5,
                moves: {
                    jab: { startup: 2, endlag: 16, damage: 3, type: 'normal' },
                    ftilt: { startup: 5, endlag: 22, damage: 8, type: 'tilt' },
                    neutralB: { startup: 6, endlag: 18, damage: 8, type: 'special' },
                    sideB: { startup: 12, endlag: 22, damage: 12, type: 'special' },
                }
            }],
            ['donkey', {
                weight: 127,
                fallSpeed: 1.63,
                moves: {
                    jab: { startup: 4, endlag: 20, damage: 5, type: 'normal' },
                    ftilt: { startup: 7, endlag: 25, damage: 12, type: 'tilt' },
                    neutralB: { startup: 10, endlag: 25, damage: 16, type: 'special' },
                    sideB: { startup: 15, endlag: 30, damage: 18, type: 'special' }
                }
            }]
            // 他のキャラクターも同様に定義
        ]);
    }

    // 分析メイン処理
    async analyzeGameState(gameState) {
        try {
            // 入力値の検証
            this.validateGameState(gameState);

            // 各要素の分析を並行処理
            const [positionAnalysis, damageAnalysis, guardAnalysis] = await Promise.all([
                this.analyzePosition(gameState.position),
                this.analyzeDamageState(gameState.damage, gameState.character),
                this.analyzeGuardState(gameState.guardDurability, gameState.character)
            ]);

            // 総合的な推奨アクションの生成
            const recommendedActions = this.generateRecommendedActions({
                position: positionAnalysis,
                damage: damageAnalysis,
                guard: guardAnalysis,
                character: gameState.character
            });

            return {
                position: positionAnalysis,
                damage: damageAnalysis,
                guard: guardAnalysis,
                recommendedActions: recommendedActions
            };

        } catch (error) {
            console.error('Analysis failed:', error);
            throw new Error('分析処理に失敗しました');
        }
    }

    // 入力値の検証
    validateGameState(gameState) {
        if (!gameState) {
            throw new Error('ゲーム状態が提供されていません');
        }

        const requiredFields = ['position', 'damage', 'character', 'guardDurability'];
        for (const field of requiredFields) {
            if (!(field in gameState)) {
                throw new Error(`${field}が見つかりません`);
            }
        }

        // ダメージ値の検証
        if (gameState.damage.player < 0 || gameState.damage.player > 999) {
            throw new Error('プレイヤーのダメージ値が範囲外です');
        }
        if (gameState.damage.opponent < 0 || gameState.damage.opponent > 999) {
            throw new Error('相手のダメージ値が範囲外です');
        }

        // ガード耐久値の検証
        if (gameState.guardDurability < 0 || gameState.guardDurability > 100) {
            throw new Error('ガード耐久値が範囲外です');
        }
    }

    // 位置関係の分析
    analyzePosition(position) {
        const analysis = {
            advantage: 'neutral',
            reasons: [],
            score: 0
        };

        // ステージ中央からの距離を計算
        const playerCenterDist = this.calculateDistance(position.player, this.config.stage.center);
        const opponentCenterDist = this.calculateDistance(position.opponent, this.config.stage.center);

        // 中央優位性の判定
        if (playerCenterDist < opponentCenterDist) {
            analysis.score += 1;
            analysis.reasons.push('中央優位');
        }

        // 高度優位性の判定
        if (position.player.y > position.opponent.y) {
            analysis.score += 0.5;
            analysis.reasons.push('高度優位');
        }

        // ブラストゾーンとの距離を分析
        if (this.isNearBlastZone(position.opponent)) {
            analysis.score += 1.5;
            analysis.reasons.push('相手がブラストゾーン付近');
        }

        // 総合的な優位性判定
        analysis.advantage = this.calculateAdvantageState(analysis.score);

        return analysis;
    }

    // ダメージ状態の分析
    analyzeDamageState(damage, character) {
        const analysis = {
            playerState: this.getDamageState(damage.player),
            opponentState: this.getDamageState(damage.opponent),
            recommendations: []
        };

        // プレイヤーの状態に基づく分析
        if (damage.player > this.config.thresholds.damage.critical) {
            analysis.recommendations.push('復帰優先');
        } else if (damage.player > this.config.thresholds.damage.high) {
            analysis.recommendations.push('防御重視');
        }

        // 相手の状態に基づく分析
        if (damage.opponent > this.config.thresholds.damage.critical) {
            analysis.recommendations.push('フィニッシュ技を狙う');
        } else if (damage.opponent > this.config.thresholds.damage.high) {
            analysis.recommendations.push('エッジガード有効');
        }

        return analysis;
    }

    // ガード状態の分析
    analyzeGuardState(guardDurability, character) {
        const analysis = {
            status: this.getGuardStatus(guardDurability),
            canGuardCancel: false,
            availableMoves: [],
            recommendations: []
        };

        // ガード耐久値に基づく推奨
        if (guardDurability < this.config.thresholds.guard.danger) {
            analysis.recommendations.push('シールド破壊に注意');
        } else if (guardDurability < this.config.thresholds.guard.warning) {
            analysis.recommendations.push('シールドを控えめに');
        }

        // ガーキャン可能な技の判定
        const characterData = this.characterData.get(character.player);
        if (characterData) {
            analysis.availableMoves = this.getAvailableGuardCancelMoves(characterData.moves, guardDurability);
            analysis.canGuardCancel = analysis.availableMoves.length > 0;
        }

        return analysis;
    }

    // 推奨アクションの生成
    generateRecommendedActions(analysisResults) {
        const { position, damage, guard, character } = analysisResults;
        const actions = [];

        // 位置ベースの推奨
        if (position.advantage === 'disadvantage') {
            actions.push('中央への移動を意識');
        } else if (position.advantage === 'advantage') {
            actions.push('有利を活かした攻め継続');
        }

        // ダメージベースの推奨
        actions.push(...damage.recommendations);

        // ガードベースの推奨
        actions.push(...guard.recommendations);

        // キャラクター特性を考慮した推奨
        const characterData = this.characterData.get(character.player);
        if (characterData) {
            // キャラクター固有の推奨事項を追加
        }

        return this.prioritizeActions(actions);
    }

    // ユーティリティメソッド
    calculateDistance(point1, point2) {
        return Math.sqrt(
            Math.pow(point2.x - point1.x, 2) + 
            Math.pow(point2.y - point1.y, 2)
        );
    }

    isNearBlastZone(position) {
        const margin = 30; // ブラストゾーン判定のマージン
        const { blastZones } = this.config.stage;

        return (
            Math.abs(position.x) > Math.abs(blastZones.left) - margin ||
            position.y > blastZones.top - margin ||
            position.y < blastZones.bottom + margin
        );
    }

    calculateAdvantageState(score) {
        if (score >= 2) return 'significant_advantage';
        if (score >= 1) return 'advantage';
        if (score <= -2) return 'significant_disadvantage';
        if (score <= -1) return 'disadvantage';
        return 'neutral';
    }

    getDamageState(damage) {
        const { thresholds } = this.config;
        if (damage > thresholds.damage.critical) return 'critical';
        if (damage > thresholds.damage.high) return 'high';
        if (damage > thresholds.damage.medium) return 'medium';
        if (damage > thresholds.damage.low) return 'low';
        return 'safe';
    }

    getGuardStatus(guardDurability) {
        const { thresholds } = this.config;
        if (guardDurability < thresholds.guard.danger) return 'danger';
        if (guardDurability < thresholds.guard.warning) return 'warning';
        return 'safe';
    }

    getAvailableGuardCancelMoves(moves, guardDurability) {
        return Object.entries(moves)
            .filter(([_, move]) => {
                return move.startup <= this.calculateGuardCancelWindow(guardDurability);
            })
            .map(([name, move]) => ({
                name,
                startup: move.startup,
                endlag: move.endlag,
                damage: move.damage
            }));
    }

    calculateGuardCancelWindow(guardDurability) {
        // ガード耐久値に基づいてガーキャン可能フレームを計算
        return Math.floor(10 * (guardDurability / 100));
    }

    prioritizeActions(actions) {
        // 重複を除去し、優先順位の高い行動を先頭に
        return [...new Set(actions)];
    }
}

// エクスポート
export default SmashAnalyzer;