import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Table, Button, Modal, Form, Input, Select, InputNumber, Tag, message, Space, Upload } from 'antd';
import { PlusOutlined, EditOutlined, ReloadOutlined, UploadOutlined, ArrowLeftOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';

import apiService from '../../services/api';
import { MenuItem } from '../../types';

export const AdminDashboardScreen = () => {
    const navigate = useNavigate();
    const [items, setItems] = useState<MenuItem[]>([]);
    const [filteredItems, setFilteredItems] = useState<MenuItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingItem, setEditingItem] = useState<MenuItem | null>(null);
    const [form] = Form.useForm();
    const [searchText, setSearchText] = useState('');


    // Fetch items on mount
    useEffect(() => {
        fetchItems();
    }, []);

    // Filter items when searchText changes
    useEffect(() => {
        const filtered = items.filter(item =>
            item.item_name.toLowerCase().includes(searchText.toLowerCase())
        );
        setFilteredItems(filtered);
    }, [searchText, items]);

    const fetchItems = async () => {
        setLoading(true);
        try {
            const data = await apiService.getMenuItems();
            setItems(data);
            setFilteredItems(data); // Initialize filtered items
        } catch (error) {
            message.error('Failed to load menu items');
        } finally {
            setLoading(false);
        }
    };

    const handleAdd = () => {
        setEditingItem(null);
        form.resetFields();
        setModalVisible(true);
    };

    const handleEdit = (record: MenuItem) => {
        setEditingItem(record);
        form.setFieldsValue({
            ...record,
            // Ensure nested suitability data is preserved logic is handled in onFinish
        });
        setModalVisible(true);
    };

    const handleSave = async (values: any) => {
        try {
            const payload = {
                ...values,
                // Preserve suitable_for from editingItem or use safe defaults for new items
                suitable_for: editingItem?.suitable_for || {
                    bmi_categories: ["underweight", "normal", "overweight", "obese"],
                    medical_conditions: ["none", "diabetes", "bp", "acidity"]
                }
            };

            await apiService.saveMenuItem(payload);
            message.success(`Item ${editingItem ? 'updated' : 'created'} successfully`);
            setModalVisible(false);
            fetchItems(); // Refresh data
        } catch (error) {
            message.error('Failed to save item');
        }
    };

    const handleDelete = async (record: MenuItem) => {
        try {
            await apiService.deleteMenuItem(record.item_id);
            message.success('Item deleted successfully');
            fetchItems(); // Refresh data
        } catch (error) {
            message.error('Failed to delete item');
        }
    };

    const columns = [
        {
            title: 'Image',
            dataIndex: 'image_url',
            key: 'image',
            render: (url: string, record: MenuItem) => (
                <div className="w-16 h-16 rounded-lg overflow-hidden bg-zinc-800 border border-zinc-700">
                    {url ? (
                        <img
                            src={url}
                            alt={record.item_name}
                            className="w-full h-full object-cover"
                            onError={(e) => {
                                (e.target as HTMLImageElement).style.display = 'none';
                                (e.target as HTMLImageElement).nextElementSibling?.classList.remove('hidden');
                            }}
                        />
                    ) : null}
                    <div className={`w-full h-full flex items-center justify-center ${url ? 'hidden' : ''}`}>
                        <span className="text-2xl">🍽️</span>
                    </div>
                </div>
            )
        },
        {
            title: 'Name',
            dataIndex: 'item_name',
            key: 'name',
            className: 'font-display font-bold text-lg text-white'
        },
        {
            title: 'Calories',
            dataIndex: 'calories',
            key: 'calories',
            render: (cal: number) => <span className="text-zinc-400">{cal} kcal</span>
        },
        {
            title: 'Attributes',
            key: 'attributes',
            render: (_: any, record: MenuItem) => (
                <Space direction="vertical" size={4}>
                    <Tag color={record.diet_type === 'veg' ? 'green' : 'red'}>{record.diet_type}</Tag>
                    <Tag color="orange">Spice: {record.spice_level}</Tag>
                </Space>
            )
        },
        {
            title: 'Actions',
            key: 'actions',
            render: (_: any, record: MenuItem) => (
                <Space>
                    <Button
                        type="primary"
                        icon={<EditOutlined />}
                        onClick={() => handleEdit(record)}
                        ghost
                    >
                        Edit
                    </Button>
                    <Button
                        type="primary"
                        danger
                        onClick={() => handleDelete(record)}
                    >
                        Delete
                    </Button>
                </Space>
            )
        }
    ];

    return (
        <div className="min-h-screen pt-24 px-6 pb-12 bg-black">
            <div className="max-w-7xl mx-auto space-y-8">
                {/* Header */}
                <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                    <div className="flex items-center gap-4">
                        <Button
                            type="text"
                            icon={<ArrowLeftOutlined className="text-xl" />}
                            className="text-white hover:text-dosa-heat flex items-center justify-center"
                            onClick={() => navigate('/')}
                        />
                        <h1 className="text-4xl font-display font-bold text-transparent bg-clip-text bg-gradient-to-r from-dosa-heat to-dosa-warm m-0">
                            Menu Dashboard
                        </h1>
                    </div>

                    {/* Search Bar */}
                    <div className="flex-1 max-w-md w-full">
                        <Input.Search
                            placeholder="Search items..."
                            allowClear
                            onChange={(e) => setSearchText(e.target.value)}
                            size="large"
                            className="w-full"
                        />
                    </div>

                    <Space>

                        <Button icon={<ReloadOutlined />} onClick={fetchItems} loading={loading}>
                            Refresh
                        </Button>
                        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd} size="large">
                            Add New Item
                        </Button>
                    </Space>
                </div>

                {/* Table */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="bg-zinc-900/50 backdrop-blur-xl rounded-3xl border border-zinc-800 overflow-hidden"
                >
                    <Table
                        columns={columns}
                        dataSource={filteredItems}
                        rowKey="item_id"
                        loading={loading}
                        pagination={{ pageSize: 8 }}
                        className="ant-table-dark"
                    />
                </motion.div>

                {/* Edit Modal */}
                <Modal
                    title={<span className="text-xl font-bold">{editingItem ? 'Edit Item' : 'Add New Item'}</span>}
                    open={modalVisible}
                    onCancel={() => setModalVisible(false)}
                    footer={null}
                    destroyOnClose
                    width={600}
                >
                    <Form
                        form={form}
                        layout="vertical"
                        onFinish={handleSave}
                        className="pt-4"
                    >
                        <Form.Item
                            name="item_name"
                            label="Item Name"
                            rules={[{ required: true, message: 'Please enter item name' }]}
                        >
                            <Input placeholder="e.g. Masala Dosa" size="large" />
                        </Form.Item>

                        <Form.Item
                            name="image_url"
                            label="Image"
                            extra="Upload an image or paste a URL"
                        >
                            <div className="space-y-3">
                                <Input placeholder="https://..." onChange={(e) => form.setFieldValue('image_url', e.target.value)} />
                                <Upload
                                    accept="image/*"
                                    showUploadList={false}
                                    customRequest={async ({ file, onSuccess, onError }: any) => {
                                        try {
                                            setLoading(true);
                                            const { url } = await apiService.uploadImage(file as File);
                                            form.setFieldValue('image_url', url);
                                            message.success('Image uploaded successfully');
                                            onSuccess?.(url);
                                        } catch (err) {
                                            message.error('Upload failed');
                                            onError?.(err as Error);
                                        } finally {
                                            setLoading(false);
                                        }
                                    }}
                                >
                                    <Button icon={<UploadOutlined />}>Click to Upload from Computer</Button>
                                </Upload>

                                {/* Preview */}
                                <Form.Item noStyle shouldUpdate>
                                    {() => {
                                        const url = form.getFieldValue('image_url');
                                        return url ? (
                                            <div className="mt-2 w-32 h-32 rounded-lg overflow-hidden border border-zinc-700">
                                                <img src={url} alt="Preview" className="w-full h-full object-cover" />
                                            </div>
                                        ) : null;
                                    }}
                                </Form.Item>
                            </div>
                        </Form.Item>

                        <div className="grid grid-cols-2 gap-4">
                            <Form.Item
                                name="calories"
                                label="Calories"
                                rules={[{ required: true }]}
                            >
                                <InputNumber className="w-full" min={0} max={2000} />
                            </Form.Item>

                            <Form.Item
                                name="diet_type"
                                label="Diet Type"
                                rules={[{ required: true }]}
                            >
                                <Select>
                                    <Select.Option value="veg">Veg 🥗</Select.Option>
                                    <Select.Option value="egg">Egg 🥚</Select.Option>
                                    <Select.Option value="non-veg">Non-Veg 🍗</Select.Option>
                                </Select>
                            </Form.Item>

                            <Form.Item
                                name="spice_level"
                                label="Spice Level"
                                rules={[{ required: true }]}
                            >
                                <Select>
                                    <Select.Option value="low">Low 😌</Select.Option>
                                    <Select.Option value="medium">Medium 🌶️</Select.Option>
                                    <Select.Option value="high">High 🔥</Select.Option>
                                </Select>
                            </Form.Item>

                            <Form.Item
                                name="oil_level"
                                label="Oil Level"
                                rules={[{ required: true }]}
                            >
                                <Select>
                                    <Select.Option value="low">Low</Select.Option>
                                    <Select.Option value="medium">Medium</Select.Option>
                                    <Select.Option value="high">High</Select.Option>
                                </Select>
                            </Form.Item>
                        </div>

                        <div className="flex justify-end gap-3 mt-6">
                            <Button onClick={() => setModalVisible(false)}>
                                Cancel
                            </Button>
                            <Button type="primary" htmlType="submit" className="bg-dosa-heat border-dosa-heat">
                                {editingItem ? 'Update Item' : 'Create Item'}
                            </Button>
                        </div>
                    </Form>
                </Modal>
            </div>
        </div>
    );
};
