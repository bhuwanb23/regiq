import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import EditProfileForm from '../../src/components/profile/EditProfileForm';

describe('EditProfileForm', () => {
  const mockProfile = {
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    phone: '123-456-7890',
    department: 'Compliance',
    position: 'Manager'
  };

  const mockOnSave = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders correctly with profile data', () => {
    const { getByText, getByDisplayValue } = render(
      <EditProfileForm
        profile={mockProfile}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
        loading={false}
      />
    );

    expect(getByDisplayValue('John')).toBeTruthy();
    expect(getByDisplayValue('Doe')).toBeTruthy();
    expect(getByDisplayValue('john.doe@example.com')).toBeTruthy();
    expect(getByText('Save Changes')).toBeTruthy();
    expect(getByText('Cancel')).toBeTruthy();
  });

  it('calls onSave when save button is pressed with valid data', () => {
    const { getByText } = render(
      <EditProfileForm
        profile={mockProfile}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
        loading={false}
      />
    );

    fireEvent.press(getByText('Save Changes'));
    
    expect(mockOnSave).toHaveBeenCalledWith(mockProfile);
  });

  it('calls onCancel when cancel button is pressed', () => {
    const { getByText } = render(
      <EditProfileForm
        profile={mockProfile}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
        loading={false}
      />
    );

    fireEvent.press(getByText('Cancel'));
    
    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('shows validation error when required fields are empty', () => {
    const emptyProfile = {
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      department: '',
      position: ''
    };

    const { getByText } = render(
      <EditProfileForm
        profile={emptyProfile}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
        loading={false}
      />
    );

    fireEvent.press(getByText('Save Changes'));
    
    // The onSave function should not be called when validation fails
    expect(mockOnSave).not.toHaveBeenCalled();
  });

  it('shows validation error for invalid email', () => {
    const invalidEmailProfile = {
      ...mockProfile,
      email: 'invalid-email'
    };

    const { getByText } = render(
      <EditProfileForm
        profile={invalidEmailProfile}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
        loading={false}
      />
    );

    fireEvent.press(getByText('Save Changes'));
    
    // The onSave function should not be called when validation fails
    expect(mockOnSave).not.toHaveBeenCalled();
  });
});