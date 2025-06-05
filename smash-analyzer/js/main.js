document.addEventListener('DOMContentLoaded', function() {
    const analyzer = new SmashAnalyzer();
    
    // DOM要素の取得と初期化
    const elements = {
        uploadArea: document.getElementById('uploadArea'),
        fileInput: document.getElementById('fileInput'),
        preview: document.getElementById('preview'),
        form: document.querySelector('.parameters-section'),
        inputs: {
            playerCharacter: document.getElementById('playerCharacter'),
            opponentCharacter: document.getElementById('opponentCharacter'),
            playerDamage: document.getElementById('playerDamage'),
            opponentDamage: document.getElementById('opponentDamage'),
            guardDurability: document.getElementById('guardDurability')
        },
        results: {
            position: document.getElementById('positionResult'),
            action: document.getElementById('actionResult'),
            guard: document.getElementById('guardResult')
        }
    };

    // 画像アップロード関連の処理
    function initializeUploadHandlers() {
        elements.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            elements.uploadArea.classList.add('dragover');
        });

        elements.uploadArea.addEventListener('dragleave', () => {
            elements.uploadArea.classList.remove('dragover');
        });

        elements.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            elements.uploadArea.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });

        elements.fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });
    }

    // ファイル処理
    function handleFiles(files) {
        if (!files || files.length === 0) return;
        
        const file = files[0];
        if (!file.type.startsWith('image/')) {
            showNotification('エラー: 画像ファイルをアップロードしてください', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const image = new Image();
            image.onload = () => {
                displayPreview(image);
                processImage(image);
            };
            image.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    // プレビュー表示
    function displayPreview(image) {
        elements.preview.innerHTML = '';
        const previewImage = image.cloneNode();
        previewImage.classList.add('preview-image');
        elements.preview.appendChild(previewImage);
    }

    // フォーム入力の初期化
    function initializeFormHandlers() {
        Object.values(elements.inputs).forEach(input => {
            input.addEventListener('change', () => {
                validateAndUpdate();
            });

            if (input.type === 'number') {
                // 数値入力の制限
                input.addEventListener('input', (e) => {
                    const value = parseInt(e.target.value);
                    const min = parseInt(e.target.min);
                    const max = parseInt(e.target.max);
                    
                    if (value < min) e.target.value = min;
                    if (value > max) e.target.value = max;
                });
            }
        });
    }

    // バリデーションと更新
    async function validateAndUpdate() {
        const gameState = collectGameState();
        if (!gameState) return;

        try {
            elements.form.classList.add('processing');
            const analysis = await analyzer.analyzeGameState(gameState);
            updateResults(analysis);
        } catch (error) {
            showNotification(error.message, 'error');
        } finally {
            elements.form.classList.remove('processing');
        }
    }

    // ゲーム状態の収集
    function collectGameState() {
        try {
            return {
                character: {
                    player: elements.inputs.playerCharacter.value,
                    opponent: elements.inputs.opponentCharacter.value
                },
                damage: {
                    player: parseInt(elements.inputs.playerDamage.value),
                    opponent: parseInt(elements.inputs.opponentDamage.value)
                },
                guardDurability: parseInt(elements.inputs.guardDurability.value),
                position: getPositionFromImage()
            };
        } catch (error) {
            showNotification('パラメータの取得に失敗しました', 'error');
            return null;
        }
    }

    // 画像からポジション情報を取得（仮実装）
    function getPositionFromImage() {
        // 実際の実装では画像解析を行う
        return {
            player: { x: 0, y: 0 },
            opponent: { x: 50, y: 0 }
        };
    }

    // 結果の更新
    function updateResults(analysis) {
        // 位置関係の更新
        elements.results.position.textContent = `${analysis.position.status} (${analysis.position.reasons.join(', ')})`;
        elements.results.position.className = `result ${analysis.position.status}`;

        // 推奨アクションの更新
        elements.results.action.textContent = analysis.recommendedActions.join(', ');

        // ガーキャンの更新
        const guardText = analysis.guardCancel.possible ? 
            `可能 (${analysis.guardCancel.availableMoves.map(m => m.name).join(', ')})` : 
            '不可';
        elements.results.guard.textContent = guardText;

        // アクセシビリティのための通知
        announceResults(analysis);
    }

    // スクリーンリーダー用の結果通知
    function announceResults(analysis) {
        const announcement = document.createElement('div');
        announcement.setAttribute('role', 'status');
        announcement.setAttribute('aria-live', 'polite');
        announcement.className = 'sr-only';
        announcement.textContent = `分析結果が更新されました。位置関係: ${analysis.position.status}、推奨アクション: ${analysis.recommendedActions.join(', ')}`;
        
        document.body.appendChild(announcement);
        setTimeout(() => announcement.remove(), 1000);
    }

    // 通知の表示
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.setAttribute('role', 'alert');
        notification.textContent = message;

        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 5000);
    }

    // リセット機能
    function resetForm() {
        Object.values(elements.inputs).forEach(input => {
            if (input.type === 'number') {
                input.value = input.min || 0;
            } else {
                input.selectedIndex = 0;
            }
        });
        elements.preview.innerHTML = '';
        updateResults({
            position: { status: 'neutral', reasons: [] },
            recommendedActions: [],
            guardCancel: { possible: false, availableMoves: [] }
        });
    }

    // 初期化
    initializeUploadHandlers();
    initializeFormHandlers();
});