// 数値関連のユーティリティ
export const NumberUtils = {
    // 値を指定範囲内に制限
    clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    },

    // パーセンテージを計算
    calculatePercentage(value, total) {
        return (value / total * 100).toFixed(1);
    },

    // フレーム数を秒数に変換
    framesToSeconds(frames) {
        return (frames / 60).toFixed(2);
    },

    // 秒数をフレーム数に変換
    secondsToFrames(seconds) {
        return Math.round(seconds * 60);
    }
};

// バリデーション関連のユーティリティ
export const ValidationUtils = {
    // ダメージ値の検証
    validateDamage(damage) {
        const numDamage = Number(damage);
        return {
            isValid: !isNaN(numDamage) && numDamage >= 0 && numDamage <= 999,
            message: '0から999の間で入力してください'
        };
    },

    // ガード耐久値の検証
    validateGuardDurability(value) {
        const numValue = Number(value);
        return {
            isValid: !isNaN(numValue) && numValue >= 0 && numValue <= 100,
            message: '0から100の間で入力してください'
        };
    },

    // キャラクター選択の検証
    validateCharacterSelection(character) {
        return {
            isValid: character && character.trim().length > 0,
            message: 'キャラクターを選択してください'
        };
    }
};

// 画像処理関連のユーティリティ
export const ImageUtils = {
    // 画像のリサイズ
    resizeImage(img, maxWidth, maxHeight) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        let width = img.width;
        let height = img.height;

        if (width > maxWidth) {
            height = height * (maxWidth / width);
            width = maxWidth;
        }

        if (height > maxHeight) {
            width = width * (maxHeight / height);
            height = maxHeight;
        }

        canvas.width = width;
        canvas.height = height;

        ctx.drawImage(img, 0, 0, width, height);
        return canvas.toDataURL('image/jpeg', 0.8);
    },

    // 画像のアスペクト比を維持したプレビューサイズの計算
    calculatePreviewDimensions(originalWidth, originalHeight, maxWidth, maxHeight) {
        const ratio = Math.min(maxWidth / originalWidth, maxHeight / originalHeight);
        return {
            width: Math.floor(originalWidth * ratio),
            height: Math.floor(originalHeight * ratio)
        };
    }
};

// DOM操作関連のユーティリティ
export const DOMUtils = {
    // エラーメッセージの表示
    showError(message, container, duration = 5000) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.setAttribute('role', 'alert');
        errorDiv.textContent = message;

        container.appendChild(errorDiv);

        setTimeout(() => {
            errorDiv.remove();
        }, duration);
    },

    // ロード中表示の制御
    toggleLoading(element, isLoading) {
        if (isLoading) {
            element.classList.add('loading');
            element.setAttribute('aria-busy', 'true');
        } else {
            element.classList.remove('loading');
            element.setAttribute('aria-busy', 'false');
        }
    },

    // 要素の有効/無効の切り替え
    toggleElementEnabled(element, enabled) {
        element.disabled = !enabled;
        if (enabled) {
            element.removeAttribute('aria-disabled');
        } else {
            element.setAttribute('aria-disabled', 'true');
        }
    }
};

// アニメーション関連のユーティリティ
export const AnimationUtils = {
    // 要素のフェードイン
    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.display = 'block';

        let start = null;
        function animate(timestamp) {
            if (!start) start = timestamp;
            const progress = timestamp - start;
            const opacity = Math.min(progress / duration, 1);
            
            element.style.opacity = opacity;

            if (progress < duration) {
                requestAnimationFrame(animate);
            }
        }

        requestAnimationFrame(animate);
    },

    // 要素のフェードアウト
    fadeOut(element, duration = 300) {
        return new Promise(resolve => {
            let start = null;
            function animate(timestamp) {
                if (!start) start = timestamp;
                const progress = timestamp - start;
                const opacity = Math.max(1 - (progress / duration), 0);
                
                element.style.opacity = opacity;

                if (progress < duration) {
                    requestAnimationFrame(animate);
                } else {
                    element.style.display = 'none';
                    resolve();
                }
            }

            requestAnimationFrame(animate);
        });
    }
};

// デバッグ関連のユーティリティ
export const DebugUtils = {
    // デバッグモードの制御
    isDebugMode: false,

    // デバッグログの出力
    log(message, data = null) {
        if (this.isDebugMode) {
            console.log(`[DEBUG] ${message}`, data);
        }
    },

    // パフォーマンス計測
    measurePerformance(functionToMeasure, label) {
        if (!this.isDebugMode) return functionToMeasure();

        console.time(label);
        const result = functionToMeasure();
        console.timeEnd(label);
        return result;
    }
};