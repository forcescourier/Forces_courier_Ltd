/* Table Management JavaScript - Courier Management System */
/* Specialized functions for table handling and data presentation */

(function($) {
    'use strict';

    // Namespace for table functions
    window.CourierApp = window.CourierApp || {};
    CourierApp.Tables = CourierApp.Tables || {};

    /**
     * Initialize parcel management table with enhanced features
     */
    CourierApp.Tables.initParcelsTable = function(tableId) {
        var table = CourierApp.initDataTable('#' + tableId, {
            columnDefs: [
                { targets: [0], orderable: false, className: 'text-center' }, // Checkbox column
                { targets: [1], className: 'text-center' }, // ID column
                { targets: [-1], orderable: false, className: 'text-center' } // Actions column
            ],
            order: [[2, 'desc']], // Default sort by date
            pageLength: 15,
            dom: '<"row"<"col-md-6"l><"col-md-6 text-right"B>>rtip',
            buttons: [
                {
                    text: '<i class="fas fa-plus mr-2"></i>Add New',
                    className: 'btn btn-enhanced btn-sm',
                    action: function() {
                        window.location.href = 'add-parcel.html';
                    }
                },
                {
                    text: '<i class="fas fa-upload mr-2"></i>Import',
                    className: 'btn btn-outline-enhanced btn-sm',
                    action: function() {
                        window.location.href = 'bulk-import.html';
                    }
                },
                {
                    text: '<i class="fas fa-download mr-2"></i>Export',
                    className: 'btn btn-outline-enhanced btn-sm',
                    action: function() {
                        CourierApp.Tables.exportParcels();
                    }
                }
            ]
        });

        // Initialize bulk selection
        CourierApp.initBulkSelection('#' + tableId, '.parcel-checkbox');

        return table;
    };

    /**
     * Initialize riders table
     */
    CourierApp.Tables.initRidersTable = function(tableId) {
        return CourierApp.initDataTable('#' + tableId, {
            columnDefs: [
                { targets: [0], orderable: false, className: 'text-center' },
                { targets: [-1], orderable: false, className: 'text-center' }
            ],
            order: [[1, 'asc']], // Sort by rider name
            dom: '<"row"<"col-md-6"l><"col-md-6 text-right"B>>rtip',
            buttons: [
                {
                    text: '<i class="fas fa-user-plus mr-2"></i>Add Rider',
                    className: 'btn btn-enhanced btn-sm',
                    action: function() {
                        window.location.href = 'add-rider.html';
                    }
                }
            ]
        });
    };

    /**
     * Initialize merchants table
     */
    CourierApp.Tables.initMerchantsTable = function(tableId) {
        return CourierApp.initDataTable('#' + tableId, {
            columnDefs: [
                { targets: [-1], orderable: false, className: 'text-center' }
            ],
            order: [[0, 'asc']], // Sort by merchant name
            dom: '<"row"<"col-md-6"l><"col-md-6 text-right"B>>rtip',
            buttons: [
                {
                    text: '<i class="fas fa-store mr-2"></i>Add Merchant',
                    className: 'btn btn-enhanced btn-sm',
                    action: function() {
                        window.location.href = 'add-merchant.html';
                    }
                }
            ]
        });
    };

    /**
     * Filter functionality for parcels
     */
    CourierApp.Tables.initParcelFilters = function(tableInstance) {
        // Search filter with real-time search
        $('#searchFilter').on('input', function() {
            var searchValue = $(this).val();
            tableInstance.search(searchValue).draw();
        });

        $('#statusFilter').on('change', function() {
            var status = $(this).val();
            if (status) {
                // Search in the payment details column (column 4 contains the status badge)
                tableInstance.column(4).search(status, true, false).draw();
            } else {
                tableInstance.column(4).search('').draw();
            }
        });

        $('#areaFilter').on('change', function() {
            var area = $(this).val();
            if (area) {
                // Search in the payment details column (column 4 contains area info)
                tableInstance.column(4).search(area, true, false).draw();
            } else {
                tableInstance.column(4).search('').draw();
            }
        });

        $('#dateFromFilter, #dateToFilter').on('change', function() {
            CourierApp.Tables.filterByDateRange(tableInstance);
        });
    };

    /**
     * Date range filtering for tables
     */
    CourierApp.Tables.filterByDateRange = function(tableInstance) {
        var dateFrom = $('#dateFromFilter').val();
        var dateTo = $('#dateToFilter').val();
        
        // Clear existing date filters
        $.fn.dataTable.ext.search = $.fn.dataTable.ext.search.filter(function(fn) {
            return fn.name !== 'dateRangeFilter';
        });
        
        if (dateFrom || dateTo) {
            var dateFilter = function(settings, data, dataIndex) {
                // Get the date from the parcel details column (column 1)
                var dateCol = data[1]; // Parcel Details column
                if (!dateCol) return true;
                
                // Extract date from the format "Date: 2024-01-15 10:30 AM"
                var dateMatch = dateCol.match(/Date.*?(\d{4}-\d{2}-\d{2})/);
                if (!dateMatch) return true;
                
                var rowDate = new Date(dateMatch[1]);
                var minDate = dateFrom ? new Date(dateFrom) : null;
                var maxDate = dateTo ? new Date(dateTo) : null;
                
                // Set max date to end of day
                if (maxDate) {
                    maxDate.setHours(23, 59, 59, 999);
                }
                
                if ((minDate === null && maxDate === null) ||
                    (minDate === null && rowDate <= maxDate) ||
                    (maxDate === null && rowDate >= minDate) ||
                    (rowDate >= minDate && rowDate <= maxDate)) {
                    return true;
                }
                return false;
            };
            
            // Set name for identification
            dateFilter.name = 'dateRangeFilter';
            $.fn.dataTable.ext.search.push(dateFilter);
        }
        
        tableInstance.draw();
    };

    /**
     * Export parcels data
     */
    CourierApp.Tables.exportParcels = function(format) {
        format = format || 'csv';
        CourierApp.showLoading('#exportButton', 'Exporting...');
        
        // Simulate export process
        setTimeout(function() {
            CourierApp.hideLoading('#exportButton');
            CourierApp.showToast('Export completed successfully', 'success');
            // In real implementation, this would trigger actual export
        }, 2000);
    };

    /**
     * Bulk actions for parcels
     */
    CourierApp.Tables.initBulkActions = function() {
        $('#bulkActionSelect').on('change', function() {
            var action = $(this).val();
            var selectedCount = $('.parcel-checkbox:checked').length;
            
            if (selectedCount === 0) {
                CourierApp.showToast('Please select at least one parcel', 'warning');
                $(this).val('');
                return;
            }
            
            switch(action) {
                case 'assign-rider':
                    CourierApp.Tables.showBulkAssignModal(selectedCount);
                    break;
                case 'update-status':
                    CourierApp.Tables.showBulkStatusModal(selectedCount);
                    break;
                case 'delete':
                    CourierApp.Tables.confirmBulkDelete(selectedCount);
                    break;
                default:
                    break;
            }
        });
    };

    /**
     * Show bulk assign rider modal
     */
    CourierApp.Tables.showBulkAssignModal = function(count) {
        var modalContent = `
            <p>Assign ${count} selected parcels to a rider:</p>
            <div class="form-group">
                <label for="bulkRiderSelect">Select Rider:</label>
                <select class="form-control" id="bulkRiderSelect">
                    <option value="">Choose a rider...</option>
                    <option value="rider1">John Doe - R001</option>
                    <option value="rider2">Jane Smith - R002</option>
                    <option value="rider3">Mike Johnson - R003</option>
                </select>
            </div>
            <div class="form-group">
                <label for="assignmentNotes">Assignment Notes:</label>
                <textarea class="form-control" id="assignmentNotes" rows="3" placeholder="Special instructions..."></textarea>
            </div>
        `;
        
        var buttons = `
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-enhanced" id="confirmBulkAssign">Assign Parcels</button>
        `;
        
        var modal = CourierApp.showModal('bulkAssignModal', 'Bulk Assign Rider', modalContent, buttons);
        
        modal.find('#confirmBulkAssign').on('click', function() {
            var riderId = $('#bulkRiderSelect').val();
            var notes = $('#assignmentNotes').val();
            
            if (!riderId) {
                CourierApp.showToast('Please select a rider', 'warning');
                return;
            }
            
            CourierApp.showLoading(this, 'Assigning...');
            
            setTimeout(function() {
                modal.modal('hide');
                CourierApp.showToast(`Successfully assigned ${count} parcels`, 'success');
                // Reset selections and refresh table
                $('.parcel-checkbox').prop('checked', false);
                $('.select-all-checkbox').prop('checked', false);
                CourierApp.updateBulkActionState('#parcels-table', '.parcel-checkbox');
            }, 1500);
        });
    };

    /**
     * Show bulk status update modal
     */
    CourierApp.Tables.showBulkStatusModal = function(count) {
        var modalContent = `
            <p>Update status for ${count} selected parcels:</p>
            <div class="form-group">
                <label for="bulkStatusSelect">New Status:</label>
                <select class="form-control" id="bulkStatusSelect">
                    <option value="">Select status...</option>
                    <option value="pending">Pending</option>
                    <option value="in-transit">In Transit</option>
                    <option value="delivered">Delivered</option>
                    <option value="returned">Returned</option>
                </select>
            </div>
            <div class="form-group">
                <label for="statusNotes">Status Notes:</label>
                <textarea class="form-control" id="statusNotes" rows="3" placeholder="Reason for status change..."></textarea>
            </div>
        `;
        
        var buttons = `
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-enhanced" id="confirmBulkStatus">Update Status</button>
        `;
        
        var modal = CourierApp.showModal('bulkStatusModal', 'Bulk Status Update', modalContent, buttons);
        
        modal.find('#confirmBulkStatus').on('click', function() {
            var status = $('#bulkStatusSelect').val();
            var notes = $('#statusNotes').val();
            
            if (!status) {
                CourierApp.showToast('Please select a status', 'warning');
                return;
            }
            
            CourierApp.showLoading(this, 'Updating...');
            
            setTimeout(function() {
                modal.modal('hide');
                CourierApp.showToast(`Successfully updated status for ${count} parcels`, 'success');
                $('.parcel-checkbox').prop('checked', false);
                $('.select-all-checkbox').prop('checked', false);
                CourierApp.updateBulkActionState('#parcels-table', '.parcel-checkbox');
            }, 1500);
        });
    };

    /**
     * Confirm bulk delete
     */
    CourierApp.Tables.confirmBulkDelete = function(count) {
        CourierApp.confirm(
            `Are you sure you want to delete ${count} selected parcels? This action cannot be undone.`,
            'Confirm Bulk Delete',
            function(confirmed) {
                if (confirmed) {
                    CourierApp.showToast('Deleting parcels...', 'info');
                    
                    setTimeout(function() {
                        CourierApp.showToast(`Successfully deleted ${count} parcels`, 'success');
                        $('.parcel-checkbox').prop('checked', false);
                        $('.select-all-checkbox').prop('checked', false);
                        CourierApp.updateBulkActionState('#parcels-table', '.parcel-checkbox');
                    }, 2000);
                }
            }
        );
    };

    /**
     * Initialize row actions (view, edit, delete)
     */
    CourierApp.Tables.initRowActions = function() {
        // View parcel
        $(document).on('click', '.action-view', function(e) {
            e.preventDefault();
            var parcelId = $(this).data('id');
            window.location.href = 'view-parcel.html?id=' + parcelId;
        });

        // Edit parcel
        $(document).on('click', '.action-edit', function(e) {
            e.preventDefault();
            var parcelId = $(this).data('id');
            window.location.href = 'edit-parcel.html?id=' + parcelId;
        });

        // Delete parcel
        $(document).on('click', '.action-delete', function(e) {
            e.preventDefault();
            var parcelId = $(this).data('id');
            var parcelCode = $(this).data('code') || parcelId;
            
            CourierApp.confirm(
                `Are you sure you want to delete parcel ${parcelCode}? This action cannot be undone.`,
                'Confirm Delete',
                function(confirmed) {
                    if (confirmed) {
                        CourierApp.showToast('Deleting parcel...', 'info');
                        
                        setTimeout(function() {
                            CourierApp.showToast(`Parcel ${parcelCode} deleted successfully`, 'success');
                            // Remove row from table or refresh table
                            location.reload();
                        }, 1500);
                    }
                }
            );
        });

        // Track parcel
        $(document).on('click', '.action-track', function(e) {
            e.preventDefault();
            var parcelId = $(this).data('id');
            window.location.href = 'track-parcel.html?id=' + parcelId;
        });
    };

    /**
     * Initialize quick search functionality
     */
    CourierApp.Tables.initQuickSearch = function(tableInstance) {
        CourierApp.initSearch('#quickSearch', function(query) {
            tableInstance.search(query).draw();
        });
    };

    /**
     * Status badge renderer for tables
     */
    CourierApp.Tables.renderStatusBadge = function(status) {
        var badgeClass = '';
        var displayText = status;
        
        switch(status.toLowerCase()) {
            case 'delivered':
                badgeClass = 'status-delivered';
                break;
            case 'pending':
                badgeClass = 'status-pending';
                break;
            case 'in-transit':
            case 'in transit':
                badgeClass = 'status-in-transit';
                displayText = 'In Transit';
                break;
            case 'returned':
                badgeClass = 'status-returned';
                break;
            case 'cancelled':
                badgeClass = 'status-cancelled';
                break;
            default:
                badgeClass = 'status-pending';
                break;
        }
        
        return `<span class="status-badge ${badgeClass}">${displayText}</span>`;
    };

    /**
     * Action buttons renderer for tables
     */
    CourierApp.Tables.renderActionButtons = function(parcelId, parcelCode) {
        return `
            <div class="action-buttons">
                <button class="action-btn action-btn-view action-view" data-id="${parcelId}" data-toggle="tooltip" title="View Details">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="action-btn action-btn-edit action-edit" data-id="${parcelId}" data-toggle="tooltip" title="Edit Parcel">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="action-btn action-btn-delete action-delete" data-id="${parcelId}" data-code="${parcelCode}" data-toggle="tooltip" title="Delete Parcel">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
    };

    /**
     * Refresh table functionality
     */
    CourierApp.Tables.refreshTable = function(tableSelector) {
        var table = $(tableSelector).DataTable();
        
        CourierApp.showToast('Refreshing table...', 'info', 1000);
        
        // For static tables, just clear filters and redraw
        setTimeout(function() {
            // Clear all searches and filters
            table.search('').columns().search('');
            
            // Clear any custom date filters
            $.fn.dataTable.ext.search = [];
            
            // Redraw the table
            table.draw();
            
            CourierApp.showToast('Table refreshed successfully', 'success');
        }, 500);
    };

    /**
     * Apply filters to table
     */
    CourierApp.Tables.applyFilters = function(tableInstance) {
        var search = $('#searchFilter').val();
        var status = $('#statusFilter').val();
        var area = $('#areaFilter').val();
        var dateFrom = $('#dateFromFilter').val();
        var dateTo = $('#dateToFilter').val();

        // Reset all filters first
        tableInstance.search('').columns().search('');
        
        // Clear any existing custom search functions
        $.fn.dataTable.ext.search = [];
        
        if (search) {
            tableInstance.search(search);
        }
        
        if (status) {
            // Status is in column 4 (Payment & Details column contains the status badge)
            tableInstance.column(4).search(status, true, false);
        }
        
        if (area) {
            // Area is also in column 4 (Payment & Details column)
            tableInstance.column(4).search(area, true, false);
        }
        
        // Apply date range filter if dates are provided
        if (dateFrom || dateTo) {
            CourierApp.Tables.filterByDateRange(tableInstance);
        }
        
        tableInstance.draw();
        
        CourierApp.showToast('Filters applied successfully', 'success');
    };

    /**
     * Clear all filters
     */
    CourierApp.Tables.clearFilters = function(tableInstance) {
        // Reset all filter inputs
        $('#searchFilter, #statusFilter, #areaFilter, #dateFromFilter, #dateToFilter').val('');
        
        // Reset status filter select to show placeholder
        $('#statusFilter').val('').trigger('change');
        $('#areaFilter').val('').trigger('change');
        
        // Clear all table filters
        tableInstance.search('').columns().search('');
        
        // Clear any custom date filters
        $.fn.dataTable.ext.search = [];
        
        // Redraw table
        tableInstance.draw();
        
        CourierApp.showToast('All filters cleared successfully', 'success');
    };

})(jQuery);