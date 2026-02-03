import { Modal, Card, Tag, Progress, Row, Col } from 'antd';
import { 
    HeartOutlined, 
    FireOutlined, 
    ThunderboltOutlined,
    InfoCircleOutlined,
    AlertOutlined 
} from '@ant-design/icons';
import { NutritionInfo, HealthBenefit, Allergen } from '../types';

interface NutritionDetailsProps {
    visible: boolean;
    onClose: () => void;
    itemName: string;
    nutrition?: NutritionInfo;
    healthBenefits: HealthBenefit[];
    allergens: Allergen[];
    calories: number;
    servingSize?: number;
}

/**
 * NutritionDetails Component
 * 
 * Displays detailed nutritional information, health benefits, and allergen warnings
 * in a modal format for comprehensive food item information.
 */
export const NutritionDetails: React.FC<NutritionDetailsProps> = ({
    visible,
    onClose,
    itemName,
    nutrition,
    healthBenefits,
    allergens,
    calories,
    servingSize
}) => {
    const getNutrientProgress = (value: number, max: number, color: string) => ({
        percent: Math.min((value / max) * 100, 100),
        strokeColor: color,
        format: () => `${value}g`
    });

    const getAllergenColor = (allergen: Allergen) => {
        const colors: Record<Allergen, string> = {
            gluten: 'orange',
            dairy: 'blue',
            nuts: 'red',
            soy: 'purple',
            eggs: 'yellow',
            fish: 'cyan',
            shellfish: 'magenta',
            peanuts: 'red',
            sesame: 'gold',
            none: 'green'
        };
        return colors[allergen] || 'default';
    };

    const getImportanceColor = (importance: string) => {
        const colors = {
            high: 'red',
            medium: 'orange',
            low: 'green'
        };
        return colors[importance as keyof typeof colors] || 'default';
    };

    const getHealthIcon = (category: string) => {
        const icons: Record<string, React.ReactNode> = {
            heart: <HeartOutlined />,
            digestion: <ThunderboltOutlined />,
            immunity: <InfoCircleOutlined />,
            energy: <FireOutlined />,
            weight: <AlertOutlined />
        };
        return icons[category] || <HeartOutlined />;
    };

    return (
        <Modal
            title={
                <div className="flex items-center gap-2">
                    <FireOutlined className="text-orange-400" />
                    <span>Nutritional Details: {itemName}</span>
                </div>
            }
            open={visible}
            onCancel={onClose}
            footer={null}
            width={800}
            className="nutrition-details-modal"
        >
            <div className="space-y-6">
                {/* Basic Info */}
                <Card size="small" className="bg-zinc-900/40 border-zinc-700">
                    <Row gutter={16} align="middle">
                        <Col>
                            <div className="text-center">
                                <div className="text-2xl font-bold text-orange-400">{calories}</div>
                                <div className="text-xs text-zinc-400">Calories</div>
                            </div>
                        </Col>
                        {servingSize && (
                            <Col>
                                <div className="text-center">
                                    <div className="text-lg font-semibold text-zinc-300">{servingSize}g</div>
                                    <div className="text-xs text-zinc-400">Serving Size</div>
                                </div>
                            </Col>
                        )}
                    </Row>
                </Card>

                {/* Macronutrients */}
                {nutrition && (
                    <Card 
                        title={
                            <div className="flex items-center gap-2">
                                <FireOutlined className="text-orange-400" />
                                <span>Macronutrients</span>
                            </div>
                        } 
                        size="small" 
                        className="bg-zinc-900/40 border-zinc-700"
                    >
                        <div className="space-y-4">
                            <div>
                                <div className="flex justify-between mb-2">
                                    <span className="text-sm">Protein</span>
                                    <span className="text-sm font-semibold">{nutrition.protein_g}g</span>
                                </div>
                                <Progress 
                                    {...getNutrientProgress(nutrition.protein_g, 50, '#52c41a')}
                                    size="small"
                                />
                            </div>
                            
                            <div>
                                <div className="flex justify-between mb-2">
                                    <span className="text-sm">Carbohydrates</span>
                                    <span className="text-sm font-semibold">{nutrition.carbohydrates_g}g</span>
                                </div>
                                <Progress 
                                    {...getNutrientProgress(nutrition.carbohydrates_g, 100, '#1890ff')}
                                    size="small"
                                />
                            </div>
                            
                            <div>
                                <div className="flex justify-between mb-2">
                                    <span className="text-sm">Fat</span>
                                    <span className="text-sm font-semibold">{nutrition.fat_g}g</span>
                                </div>
                                <Progress 
                                    {...getNutrientProgress(nutrition.fat_g, 50, '#faad14')}
                                    size="small"
                                />
                            </div>

                            {nutrition.fiber_g && (
                                <div>
                                    <div className="flex justify-between mb-2">
                                        <span className="text-sm">Fiber</span>
                                        <span className="text-sm font-semibold">{nutrition.fiber_g}g</span>
                                    </div>
                                    <Progress 
                                        {...getNutrientProgress(nutrition.fiber_g, 30, '#722ed1')}
                                        size="small"
                                    />
                                </div>
                            )}
                        </div>
                    </Card>
                )}

                {/* Additional Nutrients */}
                {nutrition && (
                    <Card 
                        title={
                            <div className="flex items-center gap-2">
                                <InfoCircleOutlined className="text-blue-400" />
                                <span>Additional Nutrients</span>
                            </div>
                        } 
                        size="small" 
                        className="bg-zinc-900/40 border-zinc-700"
                    >
                        <Row gutter={[16, 8]}>
                            {nutrition.sugar_g && (
                                <Col span={8}>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-pink-400">{nutrition.sugar_g}g</div>
                                        <div className="text-xs text-zinc-400">Sugar</div>
                                    </div>
                                </Col>
                            )}
                            {nutrition.sodium_mg && (
                                <Col span={8}>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-yellow-400">{nutrition.sodium_mg}mg</div>
                                        <div className="text-xs text-zinc-400">Sodium</div>
                                    </div>
                                </Col>
                            )}
                            {nutrition.cholesterol_mg !== undefined && (
                                <Col span={8}>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-red-400">{nutrition.cholesterol_mg}mg</div>
                                        <div className="text-xs text-zinc-400">Cholesterol</div>
                                    </div>
                                </Col>
                            )}
                            {nutrition.vitamin_c_mg && (
                                <Col span={8}>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-orange-400">{nutrition.vitamin_c_mg}mg</div>
                                        <div className="text-xs text-zinc-400">Vitamin C</div>
                                    </div>
                                </Col>
                            )}
                            {nutrition.iron_mg && (
                                <Col span={8}>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-purple-400">{nutrition.iron_mg}mg</div>
                                        <div className="text-xs text-zinc-400">Iron</div>
                                    </div>
                                </Col>
                            )}
                            {nutrition.calcium_mg && (
                                <Col span={8}>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-cyan-400">{nutrition.calcium_mg}mg</div>
                                        <div className="text-xs text-zinc-400">Calcium</div>
                                    </div>
                                </Col>
                            )}
                        </Row>
                    </Card>
                )}

                {/* Health Benefits */}
                {healthBenefits.length > 0 && (
                    <Card 
                        title={
                            <div className="flex items-center gap-2">
                                <HeartOutlined className="text-red-400" />
                                <span>Health Benefits</span>
                            </div>
                        } 
                        size="small" 
                        className="bg-zinc-900/40 border-zinc-700"
                    >
                        <div className="space-y-3">
                            {healthBenefits.map((benefit, index) => (
                                <div key={index} className="flex items-start gap-3">
                                    <div className="mt-1">
                                        {getHealthIcon(benefit.category)}
                                    </div>
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className="font-semibold text-zinc-200">{benefit.title}</span>
                                            <Tag 
                                                color={getImportanceColor(benefit.importance)}
                                            >
                                                {benefit.importance}
                                            </Tag>
                                        </div>
                                        <p className="text-sm text-zinc-400">{benefit.description}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </Card>
                )}

                {/* Allergens */}
                {allergens.length > 0 && (
                    <Card 
                        title={
                            <div className="flex items-center gap-2">
                                <AlertOutlined className="text-red-400" />
                                <span>Allergen Information</span>
                            </div>
                        } 
                        size="small" 
                        className="bg-zinc-900/40 border-zinc-700"
                    >
                        <div className="space-y-2">
                            {allergens.includes('none') ? (
                                <Tag color="green">
                                    ✓ No Common Allergens
                                </Tag>
                            ) : (
                                allergens.map((allergen, index) => (
                                    <Tag 
                                        key={index} 
                                        color={getAllergenColor(allergen)}
                                    >
                                        ⚠️ {allergen.charAt(0).toUpperCase() + allergen.slice(1)}
                                    </Tag>
                                ))
                            )}
                        </div>
                        <div className="mt-3 text-xs text-zinc-500">
                            Please consult with restaurant staff for severe allergies.
                        </div>
                    </Card>
                )}
            </div>
        </Modal>
    );
};
