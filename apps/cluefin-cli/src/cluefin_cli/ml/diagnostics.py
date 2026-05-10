"""
ML 모델 진단 및 데이터 품질 분석 모듈.

이 모듈은 ML 파이프라인의 문제점을 진단하고 데이터 품질을 분석하는
도구들을 제공합니다.
"""

import warnings
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

warnings.filterwarnings("ignore")


class MLDiagnostics:
    """
    ML 모델 진단 및 데이터 품질 분석 클래스.

    타겟 변수 분포, 특성 품질, 클래스 불균형 등을 분석하고
    문제점을 식별하여 개선 방안을 제시합니다.
    """

    def __init__(self):
        self.console = Console()

    def analyze_target_distribution(self, y: pd.Series, target_name: str = "target") -> Dict[str, Any]:
        """
        타겟 변수 분포를 분석하고 클래스 불균형을 확인합니다.

        Args:
            y: 타겟 변수 시리즈
            target_name: 타겟 변수명

        Returns:
            분석 결과 딕셔너리
        """
        try:
            logger.info(f"타겟 변수 '{target_name}' 분포 분석 시작")

            # 기본 통계
            value_counts = y.value_counts()
            total_samples = len(y)

            # 클래스 비율 계산
            class_ratios = y.value_counts(normalize=True)

            # 클래스 불균형 지수 계산 (Imbalance Ratio)
            if len(value_counts) == 2:
                majority_class = value_counts.max()
                minority_class = value_counts.min()
                imbalance_ratio = majority_class / minority_class if minority_class > 0 else float("inf")
            else:
                imbalance_ratio = None

            # 분석 결과
            analysis = {
                "total_samples": total_samples,
                "class_counts": value_counts.to_dict(),
                "class_ratios": class_ratios.to_dict(),
                "unique_classes": len(value_counts),
                "imbalance_ratio": imbalance_ratio,
                "is_severely_imbalanced": imbalance_ratio is not None and imbalance_ratio > 10,
                "is_moderately_imbalanced": imbalance_ratio is not None and 3 < imbalance_ratio <= 10,
                "missing_values": y.isna().sum(),
                "missing_ratio": y.isna().mean(),
            }

            # 결과 출력
            self._display_target_analysis(analysis, target_name)

            # 불균형 비율 로깅 (None일 경우 처리)
            if imbalance_ratio is not None:
                logger.info(f"타겟 변수 분석 완료: 총 {total_samples}개 샘플, 불균형 비율 {imbalance_ratio:.2f}")
            else:
                logger.info(f"타겟 변수 분석 완료: 총 {total_samples}개 샘플 (단일 클래스 또는 데이터 부족)")

            return analysis

        except Exception as e:
            logger.error(f"타겟 변수 분석 오류: {e}")
            raise

    def analyze_feature_quality(self, X: pd.DataFrame, feature_names: List[str] = None) -> Dict[str, Any]:
        """
        특성 데이터 품질을 분석합니다.

        Args:
            X: 특성 데이터프레임
            feature_names: 분석할 특성명 리스트 (None이면 모든 특성)

        Returns:
            특성 품질 분석 결과
        """
        try:
            logger.info("특성 데이터 품질 분석 시작")

            if feature_names is None:
                feature_names = X.columns.tolist()

            analysis = {
                "total_features": len(feature_names),
                "total_samples": len(X),
                "feature_quality": {},
                "problematic_features": [],
                "high_quality_features": [],
            }

            for feature in feature_names:
                if feature not in X.columns:
                    continue

                feature_data = X[feature]

                # 각 특성별 품질 지표 계산
                feature_quality = {
                    "missing_count": feature_data.isna().sum(),
                    "missing_ratio": feature_data.isna().mean(),
                    "infinite_count": np.isinf(feature_data.fillna(0)).sum(),
                    "zero_count": (feature_data == 0).sum(),
                    "zero_ratio": (feature_data == 0).mean(),
                    "unique_values": feature_data.nunique(),
                    "constant_feature": feature_data.nunique() <= 1,
                    "outlier_count": 0,
                    "outlier_ratio": 0.0,
                }

                # 이상치 검출 (IQR 방법)
                if not feature_data.empty and feature_data.dtype in ["int64", "float64"]:
                    Q1 = feature_data.quantile(0.25)
                    Q3 = feature_data.quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = (feature_data < lower_bound) | (feature_data > upper_bound)
                    feature_quality["outlier_count"] = outliers.sum()
                    feature_quality["outlier_ratio"] = outliers.mean()
                    feature_quality["q1"] = Q1
                    feature_quality["q3"] = Q3
                    feature_quality["mean"] = feature_data.mean()
                    feature_quality["std"] = feature_data.std()

                analysis["feature_quality"][feature] = feature_quality

                # 문제가 있는 특성 식별
                if (
                    feature_quality["missing_ratio"] > 0.5
                    or feature_quality["constant_feature"]
                    or feature_quality["infinite_count"] > 0
                ):
                    analysis["problematic_features"].append(feature)
                elif feature_quality["missing_ratio"] < 0.1 and not feature_quality["constant_feature"]:
                    analysis["high_quality_features"].append(feature)

            # 결과 출력
            self._display_feature_quality_analysis(analysis)

            logger.info(
                f"특성 품질 분석 완료: {len(analysis['high_quality_features'])}개 고품질, {len(analysis['problematic_features'])}개 문제 특성"
            )

            return analysis

        except Exception as e:
            logger.error(f"특성 품질 분석 오류: {e}")
            raise

    def diagnose_training_data(self, X: pd.DataFrame, y: pd.Series, feature_names: List[str] = None) -> Dict[str, Any]:
        """
        전체 학습 데이터를 진단합니다.

        Args:
            X: 특성 데이터프레임
            y: 타겟 변수 시리즈
            feature_names: 분석할 특성명 리스트

        Returns:
            종합 진단 결과
        """
        try:
            logger.info("학습 데이터 종합 진단 시작")

            # 타겟 분석
            target_analysis = self.analyze_target_distribution(y)

            # 특성 품질 분석
            feature_analysis = self.analyze_feature_quality(X, feature_names)

            # 데이터 크기 분석
            size_analysis = {
                "total_samples": len(X),
                "total_features": len(feature_names) if feature_names else len(X.columns),
                "samples_per_feature_ratio": len(X) / (len(feature_names) if feature_names else len(X.columns)),
                "sufficient_data": len(X) >= 100,  # 최소 100개 샘플 권장
                "good_sample_size": len(X) >= 1000,  # 1000개 이상 권장
            }

            # 종합 진단 결과
            diagnosis = {
                "target_analysis": target_analysis,
                "feature_analysis": feature_analysis,
                "size_analysis": size_analysis,
                "recommendations": self._generate_recommendations(target_analysis, feature_analysis, size_analysis),
            }

            # 종합 결과 출력
            self._display_comprehensive_diagnosis(diagnosis)

            logger.info("학습 데이터 종합 진단 완료")

            return diagnosis

        except Exception as e:
            logger.error(f"학습 데이터 진단 오류: {e}")
            raise

    def _display_target_analysis(self, analysis: Dict, target_name: str) -> None:
        """타겟 변수 분석 결과를 표시합니다."""

        table = Table(title=f"🎯 타겟 변수 '{target_name}' 분석 결과")
        table.add_column("지표", style="cyan")
        table.add_column("값", style="magenta")
        table.add_column("해석", style="green")

        # 기본 정보
        table.add_row("총 샘플 수", str(analysis["total_samples"]), "")
        table.add_row("고유 클래스 수", str(analysis["unique_classes"]), "")

        # 클래스별 개수와 비율
        for cls, count in analysis["class_counts"].items():
            ratio = analysis["class_ratios"][cls]
            table.add_row(f"클래스 {cls}", f"{count} ({ratio:.1%})", "")

        # 불균형 정도
        if analysis["imbalance_ratio"] is not None:
            if analysis["is_severely_imbalanced"]:
                imbalance_text = "심각한 불균형"
                style = "red"
            elif analysis["is_moderately_imbalanced"]:
                imbalance_text = "중간 정도 불균형"
                style = "yellow"
            else:
                imbalance_text = "균형적"
                style = "green"

            table.add_row("불균형 비율", f"{analysis['imbalance_ratio']:.2f}:1", f"[{style}]{imbalance_text}[/{style}]")

        # 누락값
        if analysis["missing_values"] > 0:
            table.add_row(
                "누락값", f"{analysis['missing_values']} ({analysis['missing_ratio']:.1%})", "[red]요 처리 필요[/red]"
            )

        self.console.print(table)

        # 권장사항 출력
        if analysis["is_severely_imbalanced"]:
            self.console.print(
                Panel(
                    "[red]⚠️ 심각한 클래스 불균형 감지!\n"
                    "• SMOTE 오버샘플링 적용 권장\n"
                    "• 클래스 가중치 조정 필요\n"
                    "• Stratified 샘플링 사용 권장[/red]",
                    title="클래스 불균형 경고",
                    border_style="red",
                )
            )
        elif analysis["is_moderately_imbalanced"]:
            self.console.print(
                Panel(
                    "[yellow]⚠️ 중간 정도 클래스 불균형 감지\n"
                    "• 클래스 가중치 조정 고려\n"
                    "• 성능 지표 해석 시 주의 필요[/yellow]",
                    title="클래스 불균형 주의",
                    border_style="yellow",
                )
            )

    def _display_feature_quality_analysis(self, analysis: Dict) -> None:
        """특성 품질 분석 결과를 표시합니다."""

        table = Table(title="🔍 특성 데이터 품질 분석")
        table.add_column("특성명", style="cyan")
        table.add_column("누락률", style="magenta")
        table.add_column("무한값", style="yellow")
        table.add_column("이상치율", style="green")
        table.add_column("상태", style="bold")

        for feature, quality in analysis["feature_quality"].items():
            missing_ratio = f"{quality['missing_ratio']:.1%}"
            infinite_count = str(quality["infinite_count"])
            outlier_ratio = f"{quality['outlier_ratio']:.1%}"

            # 상태 결정
            if feature in analysis["problematic_features"]:
                status = "[red]문제[/red]"
            elif feature in analysis["high_quality_features"]:
                status = "[green]양호[/green]"
            else:
                status = "[yellow]보통[/yellow]"

            table.add_row(feature[:20], missing_ratio, infinite_count, outlier_ratio, status)

        self.console.print(table)

        # 요약 통계
        summary_text = f"""
총 특성 수: {analysis["total_features"]}
고품질 특성: {len(analysis["high_quality_features"])}개
문제 특성: {len(analysis["problematic_features"])}개
품질 비율: {len(analysis["high_quality_features"]) / analysis["total_features"]:.1%}
        """

        self.console.print(Panel(summary_text.strip(), title="📊 특성 품질 요약", border_style="blue"))

        # 문제 특성 상세 정보
        if analysis["problematic_features"]:
            problem_text = "문제가 있는 특성들:\n"
            for feature in analysis["problematic_features"][:5]:  # 최대 5개만 표시
                quality = analysis["feature_quality"][feature]
                problem_text += f"• {feature}: "
                issues = []
                if quality["missing_ratio"] > 0.5:
                    issues.append(f"누락률 {quality['missing_ratio']:.1%}")
                if quality["constant_feature"]:
                    issues.append("상수 특성")
                if quality["infinite_count"] > 0:
                    issues.append(f"무한값 {quality['infinite_count']}개")
                problem_text += ", ".join(issues) + "\n"

            self.console.print(Panel(problem_text.strip(), title="⚠️ 문제 특성 상세", border_style="red"))

    def _display_comprehensive_diagnosis(self, diagnosis: Dict) -> None:
        """종합 진단 결과를 표시합니다."""

        size_analysis = diagnosis["size_analysis"]

        # 데이터 크기 분석 표시
        table = Table(title="📏 데이터 크기 분석")
        table.add_column("지표", style="cyan")
        table.add_column("값", style="magenta")
        table.add_column("평가", style="green")

        table.add_row("총 샘플 수", str(size_analysis["total_samples"]), "")
        table.add_row("총 특성 수", str(size_analysis["total_features"]), "")
        table.add_row(
            "샘플/특성 비율",
            f"{size_analysis['samples_per_feature_ratio']:.1f}",
            "[green]충분[/green]" if size_analysis["samples_per_feature_ratio"] > 10 else "[red]부족[/red]",
        )

        data_adequacy = ""
        if size_analysis["good_sample_size"]:
            data_adequacy = "[green]우수한 크기[/green]"
        elif size_analysis["sufficient_data"]:
            data_adequacy = "[yellow]최소 요구사항 충족[/yellow]"
        else:
            data_adequacy = "[red]데이터 부족[/red]"

        table.add_row("데이터 충분성", "", data_adequacy)

        self.console.print(table)

        # 종합 권장사항 표시
        recommendations = diagnosis["recommendations"]
        if recommendations:
            rec_text = "\n".join(f"• {rec}" for rec in recommendations)
            self.console.print(Panel(rec_text, title="💡 개선 권장사항", border_style="blue"))

    def _generate_recommendations(
        self, target_analysis: Dict, feature_analysis: Dict, size_analysis: Dict
    ) -> List[str]:
        """분석 결과를 바탕으로 개선 권장사항을 생성합니다."""

        recommendations = []

        # 타겟 불균형 관련 권장사항
        if target_analysis["is_severely_imbalanced"]:
            recommendations.append("SMOTE나 ADASYN을 사용한 오버샘플링 적용")
            recommendations.append("클래스 가중치를 자동으로 조정하는 'balanced' 옵션 사용")
            recommendations.append("Stratified 교차 검증 사용")

        # 데이터 크기 관련 권장사항
        if not size_analysis["sufficient_data"]:
            recommendations.append("더 많은 학습 데이터 수집 (최소 100개 이상 권장)")
            recommendations.append("시계열 데이터 기간 확장")

        if size_analysis["samples_per_feature_ratio"] < 5:
            recommendations.append("특성 선택을 통한 차원 축소")
            recommendations.append("주성분 분석(PCA) 고려")

        # 특성 품질 관련 권장사항
        if feature_analysis["problematic_features"]:
            recommendations.append(f"문제 특성 {len(feature_analysis['problematic_features'])}개 제거 또는 수정")
            recommendations.append("누락값 처리 전략 개선 (평균/중앙값 대체, 보간법 등)")

        if len(feature_analysis["high_quality_features"]) / feature_analysis["total_features"] < 0.7:
            recommendations.append("특성 엔지니어링 개선")
            recommendations.append("상관관계 분석을 통한 중복 특성 제거")

        # 일반적인 권장사항
        recommendations.append("교차 검증을 통한 모델 성능 검증")
        recommendations.append("하이퍼파라미터 튜닝 수행")

        return recommendations
